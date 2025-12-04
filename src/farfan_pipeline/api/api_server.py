#!/usr/bin/env python3
"""AtroZ Dashboard API server with live pipeline integration."""

        self.jobs_dir.mkdir(parents=True, exist_ok=True)
        self.dashboard_transformer = DashboardDataService(self.jobs_dir)
        
        self.state_lock = Lock()
        self.dashboard_state = self._load_dashboard_state()
        self.region_catalog = self._build_region_catalog()
        
        self.metrics = {
            'documents_processed': 0,
            'total_questions': 0,
            'total_evidence': 0,
            'total_recommendations': 0,
            'avg_macro_score': None,
            'last_run': None,
            'pipeline_runs': [],
        }

    @calibrated_method("farfan_pipeline.api.api_server.DataService.get_pdet_regions")
    def get_pdet_regions(self) -> list[dict[str, Any]]:
        """Retrieve all PDET regions with live pipeline data from dashboard state."""
        with self.state_lock:
            region_records = [dict(record) for record in self.dashboard_state.get('regions', [])]

        total_regions = max(len(region_records), 1)
        summaries: list[dict[str, Any]] = []
        for index, record in enumerate(region_records):
            coordinates = record.get('coordinates')
            if not coordinates:
                record['coordinates'] = self._compute_region_coordinates(index, total_regions)
            summary, _ = self.dashboard_transformer.summarize_region(record)
            summaries.append(summary)

        return summaries

    @staticmethod
    def _build_region_catalog() -> dict[str, dict[str, Any]]:
        """Build catalog of PDET region metadata from official statistics."""
        catalog: dict[str, dict[str, Any]] = {}
        try:
            stats = get_subregion_statistics()
        except Exception as exc:
            logger.warning(f"Failed to load PDET statistics: {exc}")
            return catalog

        for name, info in stats.items():
            if not isinstance(info, dict):
                continue
            slug = _slugify_region_name(name)
            catalog[slug] = {
                'name': name,
                'municipalities': info.get('municipality_count', 0),
                'population': info.get('total_population', 0),
                'area': info.get('total_area_km2', 0),
                'departments': info.get('departments', []),
            }
        return catalog

    @staticmethod
    def _to_percentage(value: float | int | None, precision: int = 2) -> float | None:
        """Convert normalized scores (0-1) to percentage values."""
        if value is None:
            return None
        try:
            return round(float(value) * 100.0, precision)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _extract_macro_score(result: PipelineResult, report_payload: dict[str, Any]) -> float | None:
        """Determine macro score from pipeline result or report payload."""
        if result.macro_score is not None:
            return float(result.macro_score)

        macro_section = report_payload.get('macro_analysis')
        if isinstance(macro_section, dict):
            for key in ('overall_score', 'macro_score', 'adjusted_score', 'score'):
                value = macro_section.get(key)
                if isinstance(value, (int, float)):
                    return float(value)
                if isinstance(value, dict):
                    candidate = value.get('score') or value.get('value')
                    if isinstance(candidate, (int, float)):
                        return float(candidate)
        return None

    @staticmethod
    def _normalize_cluster_scores(raw_clusters: Any) -> dict[str, float]:
        """Normalize cluster structures into a simple slug->score mapping."""
        clusters: dict[str, float] = {}

        if isinstance(raw_clusters, dict):
            for key, value in raw_clusters.items():
                score = None
                if isinstance(value, dict):
                    score = value.get('score') or value.get('adjusted_score')
                elif isinstance(value, (int, float)):
                    score = value
                if isinstance(score, (int, float)):
                    slug = _slugify_region_name(str(key))
                    clusters[slug] = float(score)
                    clusters[str(key).lower()] = float(score)

        elif isinstance(raw_clusters, list):
            for item in raw_clusters:
                if not isinstance(item, dict):
                    continue
                score = item.get('score') or item.get('adjusted_score')
                if not isinstance(score, (int, float)):
                    continue
                identifiers = [
                    item.get('cluster_id'),
                    item.get('id'),
                    item.get('name'),
                    item.get('label'),
                ]
                for identifier in identifiers:
                    if not identifier:
                        continue
                    slug = _slugify_region_name(str(identifier))
                    clusters[slug] = float(score)
                    clusters[str(identifier).lower()] = float(score)

        return clusters

    @staticmethod
    def _extract_cluster_score(
        normalized_clusters: dict[str, float],
        candidates: list[str],
    ) -> float | None:
        """Pick the first matching cluster score using candidate identifiers."""
        for candidate in candidates:
            slug = _slugify_region_name(candidate)
            if slug in normalized_clusters:
                return normalized_clusters[slug]
            lower_key = candidate.lower()
            if lower_key in normalized_clusters:
                return normalized_clusters[lower_key]
        return None

    @staticmethod
    def _compute_region_coordinates(index: int, total: int) -> dict[str, float]:
        """Place regions on a deterministic circle layout for the dashboard."""
        if total <= 0:
            return {'x': 50.0, 'y': 50.0}

        radius = 35.0
        angle = (2 * math.pi * index) / max(total, 1)
        return {
            'x': 50.0 + radius * math.cos(angle),
            'y': 50.0 + radius * math.sin(angle),
        }

    # =====================================================================
    # Dashboard State Management
    # =====================================================================

    def _load_dashboard_state(self) -> dict[str, Any]:
        """Load persisted dashboard state from disk."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as handle:
                    state = json.load(handle)
                    state.setdefault('regions', [])
                    state.setdefault('evidence', [])
                    return state
            except Exception as exc:
                logger.warning(f"Failed to load dashboard state, resetting: {exc}")
        return {'regions': [], 'evidence': [], 'metrics': {}}

    def _persist_dashboard_state(self) -> None:
        """Persist dashboard state atomically."""
        tmp_path = self.state_file.with_suffix('.tmp')
        with open(tmp_path, 'w', encoding='utf-8') as handle:
            json.dump(self.dashboard_state, handle, indent=2, ensure_ascii=False)
        tmp_path.replace(self.state_file)

    def _store_job_artifact(self, job_id: str, payload: dict[str, Any]) -> Path:
        """Persist raw pipeline output for later retrieval."""
        job_path = self.jobs_dir / f"{job_id}.json"
        with open(job_path, 'w', encoding='utf-8') as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
        return job_path

    def _update_dashboard_state(
        self,
        job_id: str,
        result: PipelineResult,
        report_payload: dict[str, Any],
    ) -> None:
        """Merge pipeline results into dashboard state."""
        timestamp = datetime.now().isoformat()
        municipality = result.metadata.get('municipality', result.document_id)
        payload = report_payload or {}
        report_path = str(self.jobs_dir / f"{job_id}.json")

        region_name = next(
            (
                candidate
                for candidate in (
                    payload.get('region_name'),
                    payload.get('metadata', {}).get('region_name') if isinstance(payload.get('metadata'), dict) else None,
                    result.metadata.get('pdet_region'),
                    result.metadata.get('region'),
                    municipality,
                )
                if candidate
            ),
            municipality,
        )
        region_slug = _slugify_region_name(region_name)

        macro_score_raw = self._extract_macro_score(result, payload)
        cluster_payload = result.meso_scores
        if not cluster_payload:
            meso_section = payload.get('meso_analysis')
            if isinstance(meso_section, dict):
                cluster_payload = meso_section.get('cluster_scores')
        normalized_clusters = self._normalize_cluster_scores(cluster_payload)

        governance_raw = self._extract_cluster_score(normalized_clusters, ['gobernanza', 'governance', 'cl01'])
        social_raw = self._extract_cluster_score(normalized_clusters, ['social', 'cl02'])
        economic_raw = self._extract_cluster_score(normalized_clusters, ['economico', 'económico', 'economic', 'cl03'])
        environmental_raw = self._extract_cluster_score(normalized_clusters, ['ambiental', 'environmental', 'cl04'])

        raw_scores = {
            'overall': macro_score_raw,
            'governance': governance_raw,
            'social': social_raw,
            'economic': economic_raw,
            'environmental': environmental_raw,
        }
        percent_scores = {key: self._to_percentage(value) for key, value in raw_scores.items()}
        cluster_scores_percent = {
            key: self._to_percentage(value) for key, value in normalized_clusters.items()
        }

        macro_band = None
        macro_section = payload.get('macro_analysis')
        if isinstance(macro_section, dict):
            macro_band = macro_section.get('quality_band') or macro_section.get('macro_band')
        if macro_band is None:
            macro_band = result.metadata.get('macro_band')

        region_stats_ref = self.region_catalog.get(region_slug, {})
        stats_payload = {
            'municipalities': region_stats_ref.get('municipalities', 0),
            'population': region_stats_ref.get('population', 0),
            'area': region_stats_ref.get('area', 0),
            'departments': region_stats_ref.get('departments', []),
        }

        indicators_payload = {
            'alignment': percent_scores.get('overall'),
            'implementation': percent_scores.get('governance'),
            'impact': percent_scores.get('environmental') or percent_scores.get('social'),
        }

        with self.state_lock:
            regions = self.dashboard_state.setdefault('regions', [])
            region_record = next((r for r in regions if r.get('id') == region_slug), None)

            if region_record is None:
                coords = self._compute_region_coordinates(len(regions), max(1, len(regions) + 1))
                region_record = {
                    'id': region_slug,
                    'job_id': job_id,
                    'name': region_name.upper(),
                    'municipality': municipality,
                    'coordinates': coords,
                    'stats': stats_payload,
                    'raw_scores': raw_scores,
                    'scores': percent_scores,
                    'cluster_scores_raw': normalized_clusters,
                    'cluster_scores': cluster_scores_percent,
                    'indicators': indicators_payload,
                    'macro_band': macro_band,
                    'connections': list(region_stats_ref.get('connections', [])),
                    'updated_at': timestamp,
                    'latest_report': job_id,
                    'report_path': report_path,
                }
                regions.append(region_record)
            else:
                region_record['job_id'] = job_id
                region_record['latest_report'] = job_id
                region_record['name'] = region_name.upper()
                region_record['municipality'] = municipality
                region_record['stats'] = stats_payload or region_record.get('stats', {})
                region_record.setdefault('coordinates', self._compute_region_coordinates(0, max(1, len(regions))))
                region_record['raw_scores'] = raw_scores
                region_record['scores'] = percent_scores
                region_record['cluster_scores_raw'] = normalized_clusters
                region_record['cluster_scores'] = cluster_scores_percent
                region_record['indicators'] = indicators_payload
                if not region_record.get('connections'):
                    region_record['connections'] = list(region_stats_ref.get('connections', []))
                region_record['macro_band'] = macro_band
                region_record['updated_at'] = timestamp
                region_record['report_path'] = report_path

            evidence_items = self.dashboard_state.setdefault('evidence', [])
            micro = payload.get('micro_analysis', {})
            questions = micro.get('questions', [])
            for question in questions:
                for evidence in question.get('evidence', []):
                    evidence_items.append(
                        {
                            'source': evidence.get('source', 'Desconocido'),
                            'page': evidence.get('page', '?'),
                            'text': evidence.get('excerpt', ''),
                            'timestamp': timestamp,
                            'job_id': job_id,
                            'region_id': region_slug,
                        }
                    )
            evidence_items[:] = evidence_items[-200:]

            metrics = self.dashboard_state.setdefault('metrics', self.metrics)
            metrics['documents_processed'] = metrics.get('documents_processed', 0) + 1
            metrics['total_questions'] = metrics.get('total_questions', 0) + result.questions_analyzed
            metrics['total_evidence'] = metrics.get('total_evidence', 0) + result.evidence_count
            metrics['total_recommendations'] = metrics.get('total_recommendations', 0) + result.recommendations_count
            metrics['last_run'] = timestamp
            if macro_score_raw is not None:
                runs = metrics.get('pipeline_runs', [])
                runs.append(macro_score_raw)
                metrics['pipeline_runs'] = runs
                metrics['avg_macro_score'] = sum(runs) / len(runs) if runs else None

            self._persist_dashboard_state()

    # =====================================================================
    # Pipeline Execution
    # =====================================================================

    def start_pipeline_job(
        self,
        pdf_path: Path,
        municipality: str,
        settings: dict[str, Any] | None = None,
    ) -> str:
        """Kick off background pipeline execution for a PDF."""
        job_id = f"job-{uuid.uuid4().hex[:12]}"
        socketio.start_background_task(
            self._run_pipeline_job,
            job_id,
            Path(pdf_path),
            municipality,
            settings or {},
        )
        return job_id

    def _run_pipeline_job(
        self,
        job_id: str,
        pdf_path: Path,
        municipality: str,
        settings: dict[str, Any],
    ) -> None:
        """Execute pipeline in background thread and emit progress events."""

        def progress_callback(phase: int, phase_name: str) -> None:
            status = self.pipeline_connector.get_job_status(job_id) or {}
            socketio.emit(
                'analysis_progress',
                {
                    'job_id': job_id,
                    'phase': phase_name,
                    'phase_num': phase,
                    'progress': status.get('progress', 0),
                },
            )

        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.pipeline_connector.execute_pipeline(
                    pdf_path=str(pdf_path),
                    job_id=job_id,
                    municipality=municipality,
                    progress_callback=progress_callback,
                    settings=settings,
                )
            )
            report = {}
            output_path = result.metadata.get('output_path')
            if output_path and Path(output_path).exists():
                with open(output_path, 'r', encoding='utf-8') as handle:
                    report = json.load(handle)
            artifact_path = self._store_job_artifact(
                job_id,
                {
                    'pipeline_result': result.__dict__,
                    'report': report,
                },
            )
            self._update_dashboard_state(job_id, result, report or {})
            socketio.emit(
                'analysis_complete',
                {
                    'job_id': job_id,
                    'result': {
                        'macro_score': result.macro_score,
                        'meso_scores': result.meso_scores,
                        'micro_scores': result.micro_scores,
                        'report_path': str(artifact_path),
                    },
                },
            )
        except Exception as exc:
            logger.error(f"Pipeline job {job_id} failed: {exc}", exc_info=True)
            socketio.emit(
                'analysis_error',
                {
                    'job_id': job_id,
                    'error': str(exc),
                },
            )
        finally:
            asyncio.set_event_loop(None)
            loop.close()

    def get_job_status(self, job_id: str) -> dict[str, Any] | None:
        """Expose connector job status."""
        return self.pipeline_connector.get_job_status(job_id)

    def get_metrics_snapshot(self) -> dict[str, Any]:
        """Return cached metrics for admin dashboard."""
        with self.state_lock:
            metrics = dict(self.dashboard_state.get('metrics', {}))
            runs = metrics.pop('pipeline_runs', [])
            metrics['run_count'] = len(runs)
            return metrics

    @calibrated_method("farfan_core.api.api_server.DataService.get_pdet_regions")
    def get_pdet_regions(self) -> list[dict[str, Any]]:
        """
        Get all PDET regions with scores

        Returns data in format expected by AtroZ dashboard
        """
        # PDET regions from Colombian government definition
        regions = [
            {
                'id': 'alto-patia',
                'name': 'ALTO PATÍA Y NORTE DEL CAUCA',
                'coordinates': {'x': 25, 'y': 20},
                'metadata': {
                    'municipalities': 24,
                    'population': 450000,
                    'area': 12500
                },
                'scores': {
                    'overall': 72,
                    'governance': 68,
                    'social': 74,
                    'economic': 70,
                    'environmental': 75,
                    'lastUpdated': datetime.now().isoformat()
                },
                'connections': ['pacifico-medio', 'sur-tolima'],
                'indicators': {
                    'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L277_33", 0.72),
                    'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L278_38", 0.68),
                    'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L279_30", 0.75)
                }
            },
            {
                'id': 'arauca',
                'name': 'ARAUCA',
                'coordinates': {'x': 75, 'y': 15},
                'metadata': {
                    'municipalities': 4,
                    'population': 95000,
                    'area': 23818
                },
                'scores': {
                    'overall': 68,
                    'governance': 65,
                    'social': 70,
                    'economic': 67,
                    'environmental': 71,
                    'lastUpdated': datetime.now().isoformat()
                },
                'connections': ['catatumbo'],
                'indicators': {
                    'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L301_33", 0.68),
                    'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L302_38", 0.65),
                    'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L303_30", 0.70)
                }
            },
            {
                'id': 'bajo-cauca',
                'name': 'BAJO CAUCA Y NORDESTE ANTIOQUEÑO',
                'coordinates': {'x': 45, 'y': 25},
                'metadata': {'municipalities': 13, 'population': 280000, 'area': 8485},
                'scores': {'overall': 65, 'governance': 62, 'social': 66, 'economic': 64, 'environmental': 68, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['sur-cordoba', 'sur-bolivar'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L313_44", 0.65), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L313_68", 0.62), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L313_84", 0.67)}
            },
            {
                'id': 'catatumbo',
                'name': 'CATATUMBO',
                'coordinates': {'x': 65, 'y': 20},
                'metadata': {'municipalities': 11, 'population': 220000, 'area': 11700},
                'scores': {'overall': 61, 'governance': 58, 'social': 62, 'economic': 60, 'environmental': 64, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['arauca'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L322_44", 0.61), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L322_68", 0.58), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L322_84", 0.63)}
            },
            {
                'id': 'choco',
                'name': 'CHOCÓ',
                'coordinates': {'x': 15, 'y': 35},
                'metadata': {'municipalities': 14, 'population': 180000, 'area': 43000},
                'scores': {'overall': 58, 'governance': 55, 'social': 59, 'economic': 57, 'environmental': 61, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['uraba', 'pacifico-medio'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L331_44", 0.58), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L331_68", 0.55), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L331_84", 0.60)}
            },
            {
                'id': 'caguan',
                'name': 'CUENCA DEL CAGUÁN Y PIEDEMONTE CAQUETEÑO',
                'coordinates': {'x': 55, 'y': 40},
                'metadata': {'municipalities': 17, 'population': 350000, 'area': 39000},
                'scores': {'overall': 70, 'governance': 67, 'social': 71, 'economic': 69, 'environmental': 72, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['macarena', 'putumayo'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L340_44", 0.70), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L340_68", 0.67), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L340_84", 0.71)}
            },
            {
                'id': 'macarena',
                'name': 'MACARENA-GUAVIARE',
                'coordinates': {'x': 60, 'y': 55},
                'metadata': {'municipalities': 10, 'population': 140000, 'area': 32000},
                'scores': {'overall': 66, 'governance': 63, 'social': 67, 'economic': 65, 'environmental': 68, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['caguan'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L349_44", 0.66), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L349_68", 0.63), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L349_84", 0.67)}
            },
            {
                'id': 'montes-maria',
                'name': 'MONTES DE MARÍA',
                'coordinates': {'x': 40, 'y': 10},
                'metadata': {'municipalities': 15, 'population': 330000, 'area': 6500},
                'scores': {'overall': 74, 'governance': 71, 'social': 75, 'economic': 73, 'environmental': 76, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['sur-bolivar'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L358_44", 0.74), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L358_68", 0.71), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L358_84", 0.75)}
            },
            {
                'id': 'pacifico-medio',
                'name': 'PACÍFICO MEDIO',
                'coordinates': {'x': 10, 'y': 50},
                'metadata': {'municipalities': 4, 'population': 120000, 'area': 10000},
                'scores': {'overall': 62, 'governance': 59, 'social': 63, 'economic': 61, 'environmental': 64, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['choco', 'alto-patia'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L367_44", 0.62), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L367_68", 0.59), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L367_84", 0.63)}
            },
            {
                'id': 'pacifico-narinense',
                'name': 'PACÍFICO Y FRONTERA NARIÑENSE',
                'coordinates': {'x': 5, 'y': 65},
                'metadata': {'municipalities': 11, 'population': 190000, 'area': 14000},
                'scores': {'overall': 59, 'governance': 56, 'social': 60, 'economic': 58, 'environmental': 61, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['putumayo'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L376_44", 0.59), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L376_68", 0.56), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L376_84", 0.60)}
            },
            {
                'id': 'putumayo',
                'name': 'PUTUMAYO',
                'coordinates': {'x': 35, 'y': 70},
                'metadata': {'municipalities': 11, 'population': 270000, 'area': 25000},
                'scores': {'overall': 67, 'governance': 64, 'social': 68, 'economic': 66, 'environmental': 69, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['caguan', 'pacifico-narinense'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L385_44", 0.67), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L385_68", 0.64), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L385_84", 0.68)}
            },
            {
                'id': 'sierra-nevada',
                'name': 'SIERRA NEVADA - PERIJÁ - ZONA BANANERA',
                'coordinates': {'x': 70, 'y': 5},
                'metadata': {'municipalities': 10, 'population': 380000, 'area': 15000},
                'scores': {'overall': 63, 'governance': 60, 'social': 64, 'economic': 62, 'environmental': 65, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['catatumbo'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L394_44", 0.63), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L394_68", 0.60), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L394_84", 0.64)}
            },
            {
                'id': 'sur-bolivar',
                'name': 'SUR DE BOLÍVAR',
                'coordinates': {'x': 50, 'y': 15},
                'metadata': {'municipalities': 7, 'population': 150000, 'area': 7000},
                'scores': {'overall': 60, 'governance': 57, 'social': 61, 'economic': 59, 'environmental': 62, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['bajo-cauca', 'montes-maria'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L403_44", 0.60), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L403_68", 0.57), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L403_84", 0.61)}
            },
            {
                'id': 'sur-cordoba',
                'name': 'SUR DE CÓRDOBA',
                'coordinates': {'x': 35, 'y': 15},
                'metadata': {'municipalities': 5, 'population': 180000, 'area': 4500},
                'scores': {'overall': 69, 'governance': 66, 'social': 70, 'economic': 68, 'environmental': 71, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['bajo-cauca', 'uraba'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L412_44", 0.69), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L412_68", 0.66), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L412_84", 0.70)}
            },
            {
                'id': 'sur-tolima',
                'name': 'SUR DEL TOLIMA',
                'coordinates': {'x': 45, 'y': 45},
                'metadata': {'municipalities': 4, 'population': 110000, 'area': 3500},
                'scores': {'overall': 71, 'governance': 68, 'social': 72, 'economic': 70, 'environmental': 73, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['alto-patia', 'caguan'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L421_44", 0.71), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L421_68", 0.68), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L421_84", 0.72)}
            },
            {
                'id': 'uraba',
                'name': 'URABÁ ANTIOQUEÑO',
                'coordinates': {'x': 20, 'y': 10},
                'metadata': {'municipalities': 10, 'population': 420000, 'area': 11600},
                'scores': {'overall': 64, 'governance': 61, 'social': 65, 'economic': 63, 'environmental': 66, 'lastUpdated': datetime.now().isoformat()},
                'connections': ['choco', 'sur-cordoba'],
                'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L430_44", 0.64), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L430_68", 0.61), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L430_84", 0.65)}
            }
        ]
        return regions

    def get_constellation_map_data(self) -> dict[str, Any]:
        """Build constellation graph based on region and cluster relationships."""
        with self.state_lock:
            region_records = [dict(record) for record in self.dashboard_state.get('regions', [])]

        nodes: list[dict[str, Any]] = []
        links: list[dict[str, Any]] = []
        cluster_nodes: dict[str, dict[str, Any]] = {}

        for record in region_records:
            summary, context = self.dashboard_transformer.summarize_region(record)
            region_id = summary.get('id')
            if not region_id:
                continue

            nodes.append(
                {
                    'id': region_id,
                    'name': summary.get('name'),
                    'type': 'region',
                    'group': 1,
                    'score': summary.get('scores', {}).get('overall'),
                }
            )

            for cluster in context.get('clusters', []):
                cluster_id = cluster.get('cluster_id')
                if not cluster_id:
                    continue
                cluster_entry = cluster_nodes.setdefault(
                    cluster_id,
                    {
                        'id': cluster_id,
                        'name': cluster.get('name'),
                        'type': 'cluster',
                        'group': 2,
                        'score_total': 0.0,
                        'count': 0,
                    },
                )
                score_percent = cluster.get('score_percent')
                if score_percent is not None:
                    cluster_entry['score_total'] += score_percent
                    cluster_entry['count'] += 1

                links.append(
                    {
                        'source': region_id,
                        'target': cluster_id,
                        'value': score_percent if score_percent is not None else 0.0,
                    }
                )

        for cluster_id, entry in cluster_nodes.items():
            count = entry.pop('count') or 1
            score_total = entry.pop('score_total')
            entry['score'] = round(score_total / count, 2)
            nodes.append(entry)

        return {'nodes': nodes, 'links': links}

    @calibrated_method("farfan_core.api.api_server.DataService.get_region_detail")
    def get_region_detail(self, region_id: str) -> dict[str, Any] | None:
        """Get detailed region payload with macro/meso/micro layers."""
        with self.state_lock:
            region_record = None
            evidence_items: list[dict[str, Any]] = []
            for record in self.dashboard_state.get('regions', []):
                if record.get('id') == region_id:
                    region_record = dict(record)
                    break
            if region_record:
                evidence_items = [dict(item) for item in self.dashboard_state.get('evidence', []) if item.get('region_id') == region_id]

        if region_record is None:
            return None

        summary, context = self.dashboard_transformer.summarize_region(region_record)
        return self.dashboard_transformer.build_region_detail(region_record, summary, context, evidence_items)


# Initialize data service
data_service = DataService()

# Initialize recommendation engine via factory
recommendation_engine = None
try:
    recommendation_engine = create_recommendation_engine(enable_cache=True)
    logger.info("Recommendation engine initialized successfully via factory")
except Exception as e:
    logger.warning(f"Failed to initialize recommendation engine: {e}")

# Track application start time for uptime metrics
app_start_time = datetime.now()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def dashboard():
    """Serve the AtroZ dashboard"""
    from flask import send_from_directory
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': 'ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_evidence_stream", "auto_param_L572_20", 1.0).0'
    })

@app.route('/api/v1/auth/token', methods=['POST'])
@rate_limit
def get_auth_token():
    """Get authentication token"""
    data = request.get_json()
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')

    # Validate credentials (implement proper validation in production)
    if not client_id or not client_secret:
        return jsonify({'error': 'Missing credentials'}), 400

    # Generate token
    token = generate_jwt_token(client_id)

    return jsonify({
        'access_token': token,
        'token_type': 'Bearer',
        'expires_in': APIConfig.JWT_EXPIRATION_HOURS * 3600
    })

@app.route('/api/v1/constellation_map', methods=['GET'])
@rate_limit
@cache_response(timeout=300)
def get_constellation_map():
    """
    Get data for the constellation map visualization

    Returns:
        JSON object with nodes and links for the constellation map
    """
    try:
        constellation_data = data_service.get_constellation_map_data()

        return jsonify({
            'status': 'success',
            'data': constellation_data,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to get constellation map data: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/pdet/regions', methods=['GET'])
@rate_limit
@cache_response(timeout=300)
def get_pdet_regions():
    """
    Get all PDET regions with scores

    Returns:
        List of PDET regions with metadata and scores
    """
    try:
        regions = data_service.get_pdet_regions()

        return jsonify({
            'status': 'success',
            'data': regions,
            'count': len(regions),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to get PDET regions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/pdet/regions/<region_id>', methods=['GET'])
@rate_limit
@cache_response(timeout=300)
def get_region_detail(region_id: str):
    """
    Get detailed information for a specific PDET region

    Args:
        region_id: Region identifier (e.g., 'alto-patia')

    Returns:
        Detailed region data with analysis
    """
    try:
        region = data_service.get_region_detail(region_id)

        if not region:
            return jsonify({'error': 'Region not found'}), 404

        return jsonify({
            'status': 'success',
            'data': region,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to get region detail: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/municipalities/<municipality_id>', methods=['GET'])
@rate_limit
@cache_response(timeout=300)
def get_municipality_data(municipality_id: str):
    """Get REAL municipality data from PDET catalog + pipeline results."""
    from farfan_pipeline.api.pdet_colombia_data import PDET_MUNICIPALITIES, get_municipality_by_name
    
    try:
        municipality_name = municipality_id.replace('-', ' ').title()
        
        try:
            municipality = get_municipality_by_name(municipality_name)
        except ValueError:
            return jsonify({'error': f'Municipality "{municipality_name}" not found'}), 404
        
        has_analysis = False
        macro_data = None
        meso_data = []
        micro_data = []
        region_slug = _slugify_region_name(municipality.subregion.value)

        with self.state_lock:
            region_state = next(
                (dict(record) for record in self.dashboard_state.get('regions', []) if record.get('id') == region_slug),
                None,
            )

        if region_state:
            has_analysis = True

            summary, context = self.dashboard_transformer.summarize_region(region_state)
            macro_detail = context.get('macro', {})
            clusters = context.get('clusters', [])
            question_matrix = self.dashboard_transformer.extract_question_matrix(context.get('report', {}))

            macro_data = {
                'score': macro_detail.get('score'),
                'score_percent': macro_detail.get('score_percent'),
                'band': macro_detail.get('band') or summary.get('macroBand') or 'SIN DATOS',
                'coherence': macro_detail.get('coherence'),
                'systemic_gaps': macro_detail.get('systemic_gaps', []),
                'alignment': macro_detail.get('alignment'),
            }

            meso_data = [
                {
                    'cluster_id': cluster.get('cluster_id'),
                    'name': cluster.get('name'),
                    'score': cluster.get('score'),
                    'score_percent': cluster.get('score_percent'),
                    'areas': cluster.get('areas'),
                    'weakest_area': cluster.get('weakest_area'),
                    'coherence': cluster.get('coherence'),
                }
                for cluster in clusters
            ]

            micro_data = [
                {
                    'question_id': question.get('id'),
                    'policy_area': question.get('category'),
                    'dimension': question.get('dimension'),
                    'score': question.get('score'),
                    'score_percent': question.get('score_percent'),
                    'evidence': question.get('evidence'),
                    'recommendations': question.get('recommendations'),
                }
                for question in question_matrix
            ]
        
        return jsonify({
            'status': 'success',
            'municipality': {
                'id': municipality_id,
                'name': municipality.name,
                'department': municipality.department,
                'dane_code': municipality.dane_code,
                'population': municipality.population,
                'area_km2': municipality.area_km2,
                'subregion': municipality.subregion.value
            },
            'has_analysis': has_analysis,
            'macro': macro_data,
            'meso': meso_data,
            'micro': micro_data,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Failed to get municipality data: {e}")
        return jsonify({'error': str(e)}), 500

    @calibrated_method("farfan_core.api.api_server.DataService.get_evidence_stream")
    def get_evidence_stream(self) -> list[dict[str, Any]]:
        """Return normalized evidence entries for ticker display."""
        with self.state_lock:
            evidence_items = [dict(item) for item in self.dashboard_state.get('evidence', [])]
        return self.dashboard_transformer.normalize_evidence_stream(evidence_items)

@app.route('/api/v1/evidence/stream', methods=['GET'])
@rate_limit
@cache_response(timeout=60)
def get_evidence_stream():
    """
    Get evidence stream for ticker display

    Returns:
        List of evidence items with sources and timestamps
    """
    try:
        evidence = data_service.get_evidence_stream()

        return jsonify({
            'status': 'success',
            'data': evidence,
            'count': len(evidence),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to get evidence stream: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/export/dashboard', methods=['POST'])
@rate_limit
def export_dashboard_data():
    """
    Export dashboard data in various formats

    Request body:
        {
            "format": "json|csv|pdf",
            "regions": ["region_id1", "region_id2"],
            "include_evidence": true
        }

    Returns:
        Exported data file
    """
    try:
        data = request.get_json()
        export_format = data.get('format', 'json')
        region_ids = data.get('regions', [])
        include_evidence = data.get('include_evidence', False)

        # Collect data
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'regions': [],
            'evidence': [] if include_evidence else None
        }

        # Get region data
        for region_id in region_ids:
            region = data_service.get_region_detail(region_id)
            if region:
                export_data['regions'].append(region)

        # Get evidence if requested
        if include_evidence:
            export_data['evidence'] = data_service.get_evidence_stream()

        # Format response based on requested format
        if export_format == 'json':
            return jsonify({
                'status': 'success',
                'data': export_data
            })
        else:
            return jsonify({'error': f'Format {export_format} not yet implemented'}), 400

    except Exception as e:
        logger.error(f"Failed to export dashboard data: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ADMIN ENDPOINTS
# ============================================================================

@app.route('/api/admin/metrics', methods=['GET'])
@cache_response(timeout=2)
def get_admin_metrics():
    """
    Get comprehensive system metrics for admin dashboard.
    
    Returns all pipeline metrics, orchestrator stats, and performance data
    aligned with AtroZ aesthetic requirements.
    """
    try:
        with data_service.state_lock:
            metrics = data_service.dashboard_state.get('metrics', data_service.metrics)
        
        pipeline_runs = metrics.get('pipeline_runs', [])
        
        response_payload = {
            'documents_processed': metrics.get('documents_processed', 0),
            'total_questions': metrics.get('total_questions', 0),
            'total_evidence': metrics.get('total_evidence', 0),
            'total_recommendations': metrics.get('total_recommendations', 0),
            'avg_macro_score': metrics.get('avg_macro_score'),
            'last_run': metrics.get('last_run'),
            'uptime_seconds': int((datetime.now() - app_start_time).total_seconds()) if 'app_start_time' in globals() else 0,
            'calibration_version': ParameterLoaderV2.get('farfan_pipeline.api.api_server', 'calibration_version', '2.0'),
            'method_count': 300,
            'question_count': 300,
            'last_verification': metrics.get('last_run'),
            'perf_macro': metrics.get('perf_macro', 2.3),
            'perf_meso': metrics.get('perf_meso', 1.8),
            'perf_micro': metrics.get('perf_micro', 15.4),
            'perf_report': metrics.get('perf_report', 0.5),
            'estimated_time': 22,
            'pipeline_runs_count': len(pipeline_runs),
        }
        
        return jsonify(response_payload)
    
    except Exception as exc:
        logger.error(f"Failed to retrieve admin metrics: {exc}")
        return jsonify({'error': str(exc)}), 500

@app.route('/api/admin/health', methods=['GET'])
@cache_response(timeout=1)
def get_system_health():
    """
    Get real-time system health metrics (CPU, memory, cache, latency).
    
    Returns resource utilization data for AtroZ health monitor visualization.
    """
    try:
        import psutil
        
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        cache_hits = getattr(cache_response, 'hits', 0)
        cache_misses = getattr(cache_response, 'misses', 0)
        cache_total = cache_hits + cache_misses
        cache_hit_rate = (cache_hits / cache_total * 100) if cache_total > 0 else 0
        
        start_time = datetime.now()
        _ = data_service.get_pdet_regions()
        api_latency = (datetime.now() - start_time).total_seconds() * 1000
        
        return jsonify({
            'cpu': cpu_percent,
            'memory': memory.percent,
            'cache_hit_rate': cache_hit_rate,
            'api_latency': api_latency,
            'timestamp': datetime.now().isoformat(),
        })
    
    except ImportError:
        return jsonify({
            'cpu': 0,
            'memory': 0,
            'cache_hit_rate': 0,
            'api_latency': 0,
            'timestamp': datetime.now().isoformat(),
            'note': 'psutil not available',
        })
    except Exception as exc:
        logger.error(f"Failed to retrieve system health: {exc}")
        return jsonify({'error': str(exc)}), 500

@app.route('/api/admin/upload', methods=['POST'])
@require_auth
def upload_pdf_document():
    """
    Upload PDF document for pipeline analysis.
    
    Accepts multipart/form-data with 'file' field containing PDF.
    Returns document_id for subsequent analysis triggering.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        uploaded = request.files['file']
        if uploaded.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        if not uploaded.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files accepted'}), 400
        
        uploads_dir = BASE_DIR / 'data' / 'uploads'
        uploads_dir.mkdir(parents=True, exist_ok=True)
        
        document_id = f"doc-{uuid.uuid4().hex[:12]}"
        file_path = uploads_dir / f"{document_id}.pdf"
        uploaded.save(str(file_path))
        
        logger.info(f"Uploaded document: {uploaded.filename} -> {document_id}")
        
        return jsonify({
            'status': 'success',
            'document_id': document_id,
            'filename': uploaded.filename,
            'path': str(file_path),
            'timestamp': datetime.now().isoformat(),
        })
    
    except Exception as exc:
        logger.error(f"Failed to upload document: {exc}")
        return jsonify({'error': str(exc)}), 500

@app.route('/api/admin/run-analysis', methods=['POST'])
@require_auth
def trigger_pipeline_analysis():
    """
    Trigger pipeline analysis for uploaded document.
    
    Request body:
        {
            "document_id": "doc-abc123",
            "municipality": "Optional municipality name",
            "settings": {
                "phase_timeout": 300,
                "enable_cache": true,
                "enable_parallel": true,
                "log_level": "INFO"
            }
        }
    
    Returns job_id for WebSocket progress tracking.
    """
    try:
        payload = request.get_json()
        document_id = payload.get('document_id')
        
        if not document_id:
            return jsonify({'error': 'Missing document_id'}), 400
        
        uploads_dir = BASE_DIR / 'data' / 'uploads'
        pdf_path = uploads_dir / f"{document_id}.pdf"
        
        if not pdf_path.exists():
            return jsonify({'error': f'Document not found: {document_id}'}), 404
        
        municipality = payload.get('municipality', document_id)
        settings = payload.get('settings', {})
        
        job_id = data_service.start_pipeline_job(
            pdf_path=pdf_path,
            municipality=municipality,
            settings=settings,
        )
        
        logger.info(f"Pipeline analysis started: job_id={job_id}, doc={document_id}")
        
        return jsonify({
            'status': 'success',
            'job_id': job_id,
            'document_id': document_id,
            'municipality': municipality,
            'timestamp': datetime.now().isoformat(),
        })
    
    except Exception as exc:
        logger.error(f"Failed to trigger pipeline analysis: {exc}")
        return jsonify({'error': str(exc)}), 500

# ============================================================================
# WEBSOCKET HANDLERS FOR REAL-TIME UPDATES
# ============================================================================

@socketio.on('connect')
def handle_connect() -> None:
    """Handle WebSocket connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect() -> None:
    """Handle WebSocket disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('subscribe_region')
def handle_subscribe_region(data) -> None:
    """Subscribe to region updates"""
    region_id = data.get('region_id')
    logger.info(f"Client {request.sid} subscribed to region: {region_id}")

    # Send initial data
    region = data_service.get_region_detail(region_id)
    emit('region_update', region)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Handle HTTP exceptions"""
    return jsonify({
        'error': e.description,
        'status_code': e.code
    }), e.code

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {e}")
    return jsonify({
        'error': 'Internal server error',
        'message': str(e)
    }), 500

# ============================================================================
# RECOMMENDATION ENDPOINTS
# ============================================================================

@app.route('/api/v1/recommendations/micro', methods=['POST'])
@rate_limit
def generate_micro_recommendations():
    """
    Generate MICRO-level recommendations

    Request Body:
        {
            "scores": {
                "PA01-DIM01": 1.2,
                "PA02-DIM02": 1.5,
                ...
            },
            "context": {}  // Optional
        }

    Returns:
        RecommendationSet with MICRO recommendations
    """
    if not recommendation_engine:
        return jsonify({'error': 'Recommendation engine not available'}), 503

    try:
        data = request.get_json()
        scores = data.get('scores', {})
        context = data.get('context', {})

        if not scores:
            return jsonify({'error': 'Missing scores'}), 400

        rec_set = recommendation_engine.generate_micro_recommendations(scores, context)

        return jsonify({
            'status': 'success',
            'data': rec_set.to_dict(),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to generate MICRO recommendations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/recommendations/meso', methods=['POST'])
@rate_limit
def generate_meso_recommendations():
    """
    Generate MESO-level recommendations

    Request Body:
        {
            "cluster_data": {
                "CL01": {"score": 72.0, "variance": ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_evidence_stream", "auto_param_L865_52", 0.25), "weak_pa": "PA02"},
                ...
            },
            "context": {}  // Optional
        }

    Returns:
        RecommendationSet with MESO recommendations
    """
    if not recommendation_engine:
        return jsonify({'error': 'Recommendation engine not available'}), 503

    try:
        data = request.get_json()
        cluster_data = data.get('cluster_data', {})
        context = data.get('context', {})

        if not cluster_data:
            return jsonify({'error': 'Missing cluster_data'}), 400

        rec_set = recommendation_engine.generate_meso_recommendations(cluster_data, context)

        return jsonify({
            'status': 'success',
            'data': rec_set.to_dict(),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to generate MESO recommendations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/recommendations/macro', methods=['POST'])
@rate_limit
def generate_macro_recommendations():
    """
    Generate MACRO-level recommendations

    Request Body:
        {
            "macro_data": {
                "macro_band": "SATISFACTORIO",
                "clusters_below_target": ["CL02", "CL03"],
                "variance_alert": "MODERADA",
                "priority_micro_gaps": ["PA01-DIM05", "PA04-DIM04"]
            },
            "context": {}  // Optional
        }

    Returns:
        RecommendationSet with MACRO recommendations
    """
    if not recommendation_engine:
        return jsonify({'error': 'Recommendation engine not available'}), 503

    try:
        data = request.get_json()
        macro_data = data.get('macro_data', {})
        context = data.get('context', {})

        if not macro_data:
            return jsonify({'error': 'Missing macro_data'}), 400

        rec_set = recommendation_engine.generate_macro_recommendations(macro_data, context)

        return jsonify({
            'status': 'success',
            'data': rec_set.to_dict(),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to generate MACRO recommendations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/recommendations/all', methods=['POST'])
@rate_limit
def generate_all_recommendations():
    """
    Generate recommendations at all levels (MICRO, MESO, MACRO)

    Request Body:
        {
            "micro_scores": {...},
            "cluster_data": {...},
            "macro_data": {...},
            "context": {}  // Optional
        }

    Returns:
        Dictionary with MICRO, MESO, and MACRO recommendation sets
    """
    if not recommendation_engine:
        return jsonify({'error': 'Recommendation engine not available'}), 503

    try:
        data = request.get_json()
        micro_scores = data.get('micro_scores', {})
        cluster_data = data.get('cluster_data', {})
        macro_data = data.get('macro_data', {})
        context = data.get('context', {})

        all_recs = recommendation_engine.generate_all_recommendations(
            micro_scores, cluster_data, macro_data, context
        )

        return jsonify({
            'status': 'success',
            'data': {
                'MICRO': all_recs['MICRO'].to_dict(),
                'MESO': all_recs['MESO'].to_dict(),
                'MACRO': all_recs['MACRO'].to_dict()
            },
            'summary': {
                'MICRO': {
                    'total_rules': all_recs['MICRO'].total_rules_evaluated,
                    'matched': all_recs['MICRO'].rules_matched
                },
                'MESO': {
                    'total_rules': all_recs['MESO'].total_rules_evaluated,
                    'matched': all_recs['MESO'].rules_matched
                },
                'MACRO': {
                    'total_rules': all_recs['MACRO'].total_rules_evaluated,
                    'matched': all_recs['MACRO'].rules_matched
                }
            },
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to generate all recommendations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/recommendations/rules/info', methods=['GET'])
@rate_limit
@cache_response(timeout=600)
def get_rules_info():
    """
    Get information about loaded recommendation rules

    Returns:
        Statistics about loaded rules
    """
    if not recommendation_engine:
        return jsonify({'error': 'Recommendation engine not available'}), 503

    try:
        return jsonify({
            'status': 'success',
            'data': {
                'version': recommendation_engine.rules.get('version'),
                'total_rules': len(recommendation_engine.rules.get('rules', [])),
                'by_level': {
                    'MICRO': len(recommendation_engine.rules_by_level['MICRO']),
                    'MESO': len(recommendation_engine.rules_by_level['MESO']),
                    'MACRO': len(recommendation_engine.rules_by_level['MACRO'])
                },
                'rules_path': str(recommendation_engine.rules_path),
                'schema_path': str(recommendation_engine.schema_path)
            },
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to get rules info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/recommendations/reload', methods=['POST'])
@require_auth
def reload_rules():
    """
    Reload recommendation rules from disk (admin only)

    Returns:
        Success status
    """
    if not recommendation_engine:
        return jsonify({'error': 'Recommendation engine not available'}), 503

    try:
        recommendation_engine.reload_rules()

        return jsonify({
            'status': 'success',
            'message': 'Rules reloaded successfully',
            'total_rules': len(recommendation_engine.rules.get('rules', [])),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to reload rules: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    """Run API server"""
    logger.info("=" * 80)
    logger.info("AtroZ Dashboard API Server")
    logger.info("=" * 80)
    logger.info(f"CORS Origins: {APIConfig.CORS_ORIGINS}")
    logger.info(f"Rate Limiting: {APIConfig.RATE_LIMIT_ENABLED}")
    logger.info(f"Caching: {APIConfig.CACHE_ENABLED}")
    logger.info("=" * 80)

    # Run server
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('ATROZ_API_PORT', '5000')),
        debug=os.getenv('ATROZ_DEBUG', 'false').lower() == 'true'
    )

if __name__ == '__main__':
    main()
