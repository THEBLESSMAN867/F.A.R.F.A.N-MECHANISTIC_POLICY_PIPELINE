# Calibration Hardcoding Audit Report

## Executive Summary

- **Files Scanned**: 271
- **Total Violations**: 653
- **CRITICAL Violations**: 0
- **HIGH Violations**: 448
- **MEDIUM Violations**: 205
- **Files with YAML References**: 5

## Violation Categories

### Hardcoded Calibration Value (232 occurrences)

### Hardcoded Choquet Weights (6 occurrences)

### Hardcoded Layer Score (7 occurrences)

### Inline Calibration Dict (393 occurrences)

### Undeclared Bayesian Prior (1 occurrences)

### Yaml Reference (14 occurrences)

## Known Violators (Priority Review)

### src/farfan_pipeline/core/calibration/orchestrator.py

**Line 11** - `HARDCODED_CHOQUET_WEIGHTS` [MEDIUM]

*Context*: Pattern matched: choquet_integral or weighted_sum
- Applies threshold: ≥0.7 PASS, <0.7 FAIL

CRIT

```python
       9: - Reads layer requirements from canonical inventory
      10: - Computes runtime layers dynamically (@chain, @q, @d, @p, @C, @u, @m)
>>>   11: - Aggregates via choquet_integral or weighted_sum
      12: - Applies threshold: ≥0.7 PASS, <0.7 FAIL
      13: 
```

**Line 35** - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Context*: Variable 'CALIBRATION_THRESHOLD' assigned hardcoded value: 0.7

```python
      33: logger = logging.getLogger(__name__)
      34: 
>>>   35: CALIBRATION_THRESHOLD = 0.7
      36: 
      37: 
```

**Line 35** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: CALIBRATION_THRESHOLD = 0.7

```python
      33: logger = logging.getLogger(__name__)
      34: 
>>>   35: CALIBRATION_THRESHOLD = 0.7
      36: 
      37: 
```

**Line 68** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: score:.3

```python
      66:         self.threshold = threshold
      67:         super().__init__(
>>>   68:             f"Method '{method_id}' calibration score {score:.3f} is below "
      69:             f"threshold {threshold:.3f}. Method cannot be executed."
      70:         )
```

**Line 69** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: threshold:.3

```python
      67:         super().__init__(
      68:             f"Method '{method_id}' calibration score {score:.3f} is below "
>>>   69:             f"threshold {threshold:.3f}. Method cannot be executed."
      70:         )
      71: 
```

**Line 150** - `INLINE_CALIBRATION_DICT` [HIGH]

*Context*: Variable 'weights' assigned inline dict literal

```python
     148: 
     149:                 # Build weights dict
>>>  150:                 weights = {}
     151:                 for layer in required_layers:
     152:                     if layer in CHOQUET_WEIGHTS:
```

**Line 152** - `HARDCODED_CHOQUET_WEIGHTS` [MEDIUM]

*Context*: Pattern matched: CHOQUET_WEIGHTS:
                        weights[layer] = CHOQUET_WEIGHTS[layer]

```python
     150:                 weights = {}
     151:                 for layer in required_layers:
>>>  152:                     if layer in CHOQUET_WEIGHTS:
     153:                         weights[layer] = CHOQUET_WEIGHTS[layer]
     154: 
```

**Line 232** - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Context*: Variable 'score' assigned hardcoded value: 0.65

```python
     230:     def _compute_chain_score(self, context: CalibrationContext) -> float:
     231:         """Compute chain of evidence score (@chain)."""
>>>  232:         score = 0.65
     233:         if context.dimension > 0:
     234:             score += 0.15 * min(context.dimension / 10.0, 1.0)
```

**Line 232** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: score = 0.65

```python
     230:     def _compute_chain_score(self, context: CalibrationContext) -> float:
     231:         """Compute chain of evidence score (@chain)."""
>>>  232:         score = 0.65
     233:         if context.dimension > 0:
     234:             score += 0.15 * min(context.dimension / 10.0, 1.0)
```

**Line 241** - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Context*: Variable 'score' assigned hardcoded value: 0.7

```python
     239:     def _compute_quality_score(self, context: CalibrationContext) -> float:
     240:         """Compute data quality score (@q)."""
>>>  241:         score = 0.70
     242:         if context.question_num > 0:
     243:             score += 0.08 * min(context.question_num / 20.0, 1.0)
```

**Line 241** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: score = 0.70

```python
     239:     def _compute_quality_score(self, context: CalibrationContext) -> float:
     240:         """Compute data quality score (@q)."""
>>>  241:         score = 0.70
     242:         if context.question_num > 0:
     243:             score += 0.08 * min(context.question_num / 20.0, 1.0)
```

**Line 248** - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Context*: Variable 'score' assigned hardcoded value: 0.68

```python
     246:     def _compute_density_score(self, context: CalibrationContext) -> float:
     247:         """Compute data density score (@d)."""
>>>  248:         score = 0.68
     249:         if context.total_methods > 0:
     250:             ratio = context.method_position / context.total_methods
```

**Line 248** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: score = 0.68

```python
     246:     def _compute_density_score(self, context: CalibrationContext) -> float:
     247:         """Compute data density score (@d)."""
>>>  248:         score = 0.68
     249:         if context.total_methods > 0:
     250:             ratio = context.method_position / context.total_methods
```

**Line 260** - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Context*: Variable 'score' assigned hardcoded value: 0.72

```python
     258:     def _compute_coverage_score(self, context: CalibrationContext) -> float:
     259:         """Compute coverage completeness score (@C)."""
>>>  260:         score = 0.72
     261:         if context.dimension in (1, 2, 5, 10):
     262:             score += 0.1
```

**Line 260** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: score = 0.72

```python
     258:     def _compute_coverage_score(self, context: CalibrationContext) -> float:
     259:         """Compute coverage completeness score (@C)."""
>>>  260:         score = 0.72
     261:         if context.dimension in (1, 2, 5, 10):
     262:             score += 0.1
```

**Line 271** - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Context*: Variable 'score' assigned hardcoded value: 0.65

```python
     269:     def _compute_mechanism_score(self, context: CalibrationContext) -> float:
     270:         """Compute mechanistic explanation score (@m)."""
>>>  271:         score = 0.65
     272:         if context.dimension >= 7:
     273:             score += 0.15
```

**Line 271** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: score = 0.65

```python
     269:     def _compute_mechanism_score(self, context: CalibrationContext) -> float:
     270:         """Compute mechanistic explanation score (@m)."""
>>>  271:         score = 0.65
     272:         if context.dimension >= 7:
     273:             score += 0.15
```

**Line 276** - `HARDCODED_CHOQUET_WEIGHTS` [MEDIUM]

*Context*: Pattern matched: choquet_integral(
        self,
        layers: RuntimeLayers,
        weights: 

```python
     274:         return min(score, 1.0)
     275: 
>>>  276:     def choquet_integral(
     277:         self,
     278:         layers: RuntimeLayers,
```

**Line 360** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: intrinsic_score:.3

```python
     358: 
     359:         logger.debug(
>>>  360:             f"Intrinsic score for {method_id}: {intrinsic_score:.3f} "
     361:             f"(theory={intrinsic.b_theory:.3f}, impl={intrinsic.b_impl:.3f}, "
     362:             f"deploy={intrinsic.b_deploy:.3f})"
```

**Line 386** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: intrinsic_score:.3

```python
     384: 
     385:         logger.info(
>>>  386:             f"Calibration for {method_id}: intrinsic={intrinsic_score:.3f}, "
     387:             f"runtime={runtime_score:.3f}, final={final_score:.3f}"
     388:         )
```

**Line 387** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: runtime_score:.3

```python
     385:         logger.info(
     386:             f"Calibration for {method_id}: intrinsic={intrinsic_score:.3f}, "
>>>  387:             f"runtime={runtime_score:.3f}, final={final_score:.3f}"
     388:         )
     389: 
```

**Line 387** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: final_score:.3

```python
     385:         logger.info(
     386:             f"Calibration for {method_id}: intrinsic={intrinsic_score:.3f}, "
>>>  387:             f"runtime={runtime_score:.3f}, final={final_score:.3f}"
     388:         )
     389: 
```

### src/farfan_pipeline/core/calibration/layer_computers.py

**Line 141** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: score = 2.0

```python
     139:         if unit_quality < abort_threshold:
     140:             return 0.0
>>>  141:         score = 2.0 * unit_quality - 0.6
     142: 
     143:         # Validate that config produces valid result
```

**Line 156** - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Context*: Pattern matched: score = 1.0

```python
     154:         k = g_spec.get("sigmoidal_k", 5.0)
     155:         x0 = g_spec.get("sigmoidal_x0", 0.5)
>>>  156:         score = 1.0 - math.exp(-k * (unit_quality - x0))
     157: 
     158:         # Validate that config produces valid result
```

**Line 317** - `HARDCODED_LAYER_SCORE` [MEDIUM]

*Context*: Pattern matched: @m = 0.5

```python
     315: 
     316:     Spec compliance: Section 3.8
>>>  317:     Formula: x_@m = 0.5 · m_transp + 0.4 · m_gov + 0.1 · m_cost
     318: 
     319:     Args:
```

## Detailed Violations by File

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/Analyzer_one.py

**17 violation(s)**

#### Line 213 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_scores*

```python
     211:                 "cross_cutting_themes": defaultdict(list)
     212:             },
>>>  213:             "measures": {
     214:                 "semantic_density": [],
     215:                 "coherence_scores": [],
```

#### Line 278 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_scores*

```python
     276:                 "cross_cutting_themes": {}
     277:             },
>>>  278:             "measures": {
     279:                 "semantic_density": [],
     280:                 "coherence_scores": [],
```

#### Line 335 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_score*

```python
     333:             vector = vector.tolist()
     334: 
>>>  335:         return {
     336:             "segment_id": idx,
     337:             "text": segment,
```

#### Line 348 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'link_scores' assigned inline dict literal*

```python
     346:     def _classify_value_chain_link(self, segment: str) -> dict[str, float]:
     347:         """Classify segment by value chain link using keyword matching."""
>>>  348:         link_scores = {}
     349:         segment_lower = segment.lower()
     350: 
```

#### Line 372 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'domain_scores' assigned inline dict literal*

```python
     370:     def _classify_policy_domain(self, segment: str) -> dict[str, float]:
     371:         """Classify segment by policy domain using keyword matching."""
>>>  372:         domain_scores = {}
     373:         segment_lower = segment.lower()
     374: 
```

#### Line 388 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'theme_scores' assigned inline dict literal*

```python
     386:     def _classify_cross_cutting_themes(self, segment: str) -> dict[str, float]:
     387:         """Classify segment by cross-cutting themes."""
>>>  388:         theme_scores = {}
     389:         segment_lower = segment.lower()
     390: 
```

#### Line 466 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: efficiency_score*

```python
     464: 
     465:         if not segments:
>>>  466:             return {
     467:                 "throughput": ParameterLoaderV2.get("farfan_core.analysis.Analyzer_one.PerformanceAnalyzer._calculate_throughput_metrics", "auto_param_L466_30", 0.0),
     468:                 "efficiency_score": ParameterLoaderV2.get("farfan_core.analysis.Analyzer_one.PerformanceAnalyzer._calculate_throughput_metrics", "auto_param_L467_36", 0.0),
```

#### Line 493 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: efficiency_score*

```python
     491:             throughput = len(segments) * avg_coherence * sum(link_config.conversion_rates.values()) / len(link_config.conversion_rates)
     492: 
>>>  493:         return {
     494:             "throughput": float(throughput),
     495:             "efficiency_score": float(efficiency_score),
```

#### Line 504 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: bottleneck_scores*

```python
     502:         """Detect bottlenecks in value chain link."""
     503: 
>>>  504:         bottleneck_analysis = {
     505:             "capacity_constraints": {},
     506:             "bottleneck_scores": {}
```

#### Line 528 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
     526:                 score = mentions / len(segments)
     527: 
>>>  528:             bottleneck_analysis["bottleneck_scores"][bottleneck_type] = {
     529:                 "score": score,
     530:                 "severity": "high" if score > ParameterLoaderV2.get("farfan_core.analysis.Analyzer_one.PerformanceAnalyzer._detect_bottlenecks", "auto_param_L529_46", 0.2) else "medium" if score > ParameterLoaderV2.get("farfan_core.analysis.Analyzer_one.PerformanceAnalyzer._detect_bottlenecks", "auto_param_L529_75", 0.1) else "low"
```

#### Line 578 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
     576:         for link_name, metrics in performance_analysis["value_chain_metrics"].items():
     577:             if metrics["efficiency_score"] < ParameterLoaderV2.get("farfan_core.analysis.Analyzer_one.PerformanceAnalyzer._generate_recommendations", "auto_param_L576_45", 0.5):
>>>  578:                 recommendations.append({
     579:                     "link": link_name,
     580:                     "type": "efficiency_improvement",
```

#### Line 586 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
     584: 
     585:             if metrics["throughput"] < 20:
>>>  586:                 recommendations.append({
     587:                     "link": link_name,
     588:                     "type": "throughput_optimization",
```

#### Line 646 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: criticality_score*

```python
     644:             interventions = self._generate_interventions(link_name, risk_assessment, text_analysis)
     645: 
>>>  646:             diagnosis_results["critical_links"][link_name] = {
     647:                 "criticality_score": criticality_score,
     648:                 "text_analysis": text_analysis
```

#### Line 895 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: average_efficiency_score*

```python
     893:                 "policy_domains_covered": policy_domain_coverage
     894:             },
>>>  895:             "performance_summary": {
     896:                 "average_efficiency_score": float(avg_efficiency),
     897:                 "recommendations_count": len(performance_analysis["optimization_recommendations"])
```

#### Line 1610 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: Efficiency_Score*

```python
    1608: 
    1609:                 for link, metrics in perf_analysis.get('value_chain_metrics', {}).items():
>>> 1610:                     perf_data.append({
    1611:                         'Value_Chain_Link': link,
    1612:                         'Efficiency_Score': metrics.get('efficiency_score', 0),
```

#### Line 1626 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: Priority*

```python
    1624: 
    1625:                 for i, rec in enumerate(recommendations):
>>> 1626:                     rec_data.append({
    1627:                         'Recommendation_ID': i + 1,
    1628:                         'Link': rec.get('link', ''),
```

#### Line 1743 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: criticality_threshold, efficiency_threshold, throughput_threshold*

```python
    1741:                 "segmentation_method": "sentence"
    1742:             },
>>> 1743:             "analysis": {
    1744:                 "criticality_threshold": ParameterLoaderV2.get("farfan_core.analysis.Analyzer_one.ConfigurationManager.load_config", "auto_param_L1743_41", 0.4),
    1745:                 "efficiency_threshold": ParameterLoaderV2.get("farfan_core.analysis.Analyzer_one.ConfigurationManager.load_config", "auto_param_L1744_40", 0.5),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/bayesian_multilevel_system.py

**14 violation(s)**

#### Line 373 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: evidence_weight:.4*

```python
     371:                 f"{update.likelihood_ratio:.4f}",
     372:                 f"{update.posterior:.4f}",
>>>  373:                 f"{update.evidence_weight:.4f}"
     374:             ])
     375: 
```

#### Line 610 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     608: 
     609:         narrative = (
>>>  610:             f"Score of {score:.2f} is {performance} peer average "
     611:             f"({peer_mean:.2f} ± {peer_std:.2f}), "
     612:             f"placing in the {rank} (percentile: {percentile:.1%})"
```

#### Line 704 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: raw_meso_score:.4*

```python
     702:             rows.append([
     703:                 analysis.cluster_id,
>>>  704:                 f"{analysis.raw_meso_score:.4f}",
     705:                 f"{analysis.dispersion_penalty:.4f}",
     706:                 f"{analysis.peer_penalty:.4f}",
```

#### Line 708 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.4*

```python
     706:                 f"{analysis.peer_penalty:.4f}",
     707:                 f"{analysis.total_penalty:.4f}",
>>>  708:                 f"{analysis.adjusted_score:.4f}",
     709:                 f"{analysis.dispersion_metrics.get('cv', ParameterLoaderV2.get("farfan_core.analysis.bayesian_multilevel_system.BayesianRollUp.__init__", "auto_param_L709_57", 0.0)):.4f}",
     710:                 f"{analysis.dispersion_metrics.get('max_gap', ParameterLoaderV2.get("farfan_core.analysis.bayesian_multilevel_system.BayesianRollUp.__init__", "auto_param_L710_62", 0.0)):.4f}",
```

#### Line 767 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.2*

```python
     765:                     severity=severity,
     766:                     description=f"Micro question {micro.question_id} score "
>>>  767:                                f"({micro.adjusted_score:.2f}) differs significantly from "
     768:                                f"meso cluster {meso_analysis.cluster_id} "
     769:                                f"({meso_analysis.adjusted_score:.2f})"
```

#### Line 769 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.2*

```python
     767:                                f"({micro.adjusted_score:.2f}) differs significantly from "
     768:                                f"meso cluster {meso_analysis.cluster_id} "
>>>  769:                                f"({meso_analysis.adjusted_score:.2f})"
     770:                 )
     771: 
```

#### Line 799 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.2*

```python
     797:                     severity=severity,
     798:                     description=f"Meso cluster {meso.cluster_id} score "
>>>  799:                                f"({meso.adjusted_score:.2f}) differs significantly from "
     800:                                f"macro overall ({macro_score:.2f})"
     801:                 )
```

#### Line 800 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: macro_score:.2*

```python
     798:                     description=f"Meso cluster {meso.cluster_id} score "
     799:                                f"({meso.adjusted_score:.2f}) differs significantly from "
>>>  800:                                f"macro overall ({macro_score:.2f})"
     801:                 )
     802: 
```

#### Line 939 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.3*

```python
     937:             f"dispersion_pen={dispersion_penalty:.3f}, "
     938:             f"contradiction_pen={contradiction_penalty:.3f}, "
>>>  939:             f"final={adjusted_score:.3f}"
     940:         )
     941: 
```

#### Line 1019 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: coverage_score:.4*

```python
    1017:             [
    1018:                 'coverage',
>>> 1019:                 f"{macro_analysis.coverage_score:.4f}",
    1020:                 f"{macro_analysis.coverage_penalty:.4f}",
    1021:                 'Question coverage ratio'
```

#### Line 1025 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: dispersion_score:.4*

```python
    1023:             [
    1024:                 'dispersion',
>>> 1025:                 f"{macro_analysis.dispersion_score:.4f}",
    1026:                 f"{macro_analysis.dispersion_penalty:.4f}",
    1027:                 'Portfolio dispersion score'
```

#### Line 1037 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.4*

```python
    1035:             [
    1036:                 'adjusted_score',
>>> 1037:                 f"{macro_analysis.adjusted_score:.4f}",
    1038:                 'ParameterLoaderV2.get("farfan_core.analysis.bayesian_multilevel_system.BayesianPortfolioComposer.__init__", "auto_param_L1038_17", 0.0000)',
    1039:                 'Final penalty-adjusted score'
```

#### Line 1126 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.4*

```python
    1124:         self.logger.info("\n" + "=" * 80)
    1125:         self.logger.info("ANALYSIS COMPLETE")
>>> 1126:         self.logger.info(f"Final adjusted score: {macro_analysis.adjusted_score:.4f}")
    1127:         self.logger.info(f"Outputs saved to: {self.output_dir}")
    1128:         self.logger.info("=" * 80)
```

#### Line 1277 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.4*

```python
    1275: 
    1276:         self.logger.info(f"  Detected {macro_analysis.contradiction_count} contradictions")
>>> 1277:         self.logger.info(f"  Final macro score: {macro_analysis.adjusted_score:.4f}")
    1278: 
    1279:         return macro_analysis
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/contradiction_deteccion.py

**12 violation(s)**

#### Line 39 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: runtime error fixes for defensive programming
from farfan_pipeline.utils.runtime*

```python
      37: from farfan_pipeline.core.dependency_lockdown import get_dependency_lockdown
      38: 
>>>   39: # Import runtime error fixes for defensive programming
      40: from farfan_pipeline.utils.runtime_error_fixes import ensure_list_return, safe_text_extract
      41: from farfan_pipeline.core.parameters import ParameterLoaderV2
```

#### Line 643 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: domain_weight=1.5*

```python
     641:                                             evidence_strength=1 - p_value,
     642:                                             observations=2,
>>>  643:                                             domain_weight=1.5  # Mayor peso para evidencia numérica
     644:                                         )
     645: 
```

#### Line 688 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: domain_weight=1.2*

```python
     686:                     evidence_strength=ParameterLoaderV2.get("farfan_core.analysis.contradiction_deteccion.PolicyContradictionDetector._build_knowledge_graph", "auto_param_L686_38", 0.9),  # Alta confianza en lógica temporal
     687:                     observations=len(conflicts),
>>>  688:                     domain_weight=1.2
     689:                 )
     690: 
```

#### Line 796 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: domain_weight=1.3*

```python
     794:                                     evidence_strength=ParameterLoaderV2.get("farfan_core.analysis.contradiction_deteccion.PolicyContradictionDetector._build_knowledge_graph", "auto_param_L794_54", 0.8),
     795:                                     observations=len(allocations),
>>>  796:                                     domain_weight=1.3
     797:                                 )
     798: 
```

#### Line 863 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_score, objective_alignment*

```python
     861:         syntactic_complexity = self._calculate_syntactic_complexity(text)
     862: 
>>>  863:         return {
     864:             "coherence_score": float(coherence_score),
     865:             "contradiction_density": float(contradiction_density),
```

#### Line 1050 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
    1048:         for cont_type, conflicts in by_type.items():
    1049:             if cont_type == ContradictionType.NUMERICAL_INCONSISTENCY:
>>> 1050:                 recommendations.append({
    1051:                     "type": "numerical_reconciliation",
    1052:                     "priority": "high",
```

#### Line 1063 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
    1061: 
    1062:             elif cont_type == ContradictionType.TEMPORAL_CONFLICT:
>>> 1063:                 recommendations.append({
    1064:                     "type": "timeline_adjustment",
    1065:                     "priority": "high",
```

#### Line 1076 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
    1074: 
    1075:             elif cont_type == ContradictionType.RESOURCE_ALLOCATION_MISMATCH:
>>> 1076:                 recommendations.append({
    1077:                     "type": "budget_reallocation",
    1078:                     "priority": "critical",
```

#### Line 1089 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
    1087: 
    1088:             elif cont_type == ContradictionType.SEMANTIC_OPPOSITION:
>>> 1089:                 recommendations.append({
    1090:                     "type": "conceptual_clarification",
    1091:                     "priority": "medium",
```

#### Line 1102 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'priority_order' assigned inline dict literal*

```python
    1100: 
    1101:         # Ordenar por prioridad
>>> 1102:         priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    1103:         recommendations.sort(key=lambda x: priority_order.get(x["priority"], 4))
    1104: 
```

#### Line 1128 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: logical_conflict_score*

```python
    1126:     ) -> dict[str, Any]:
    1127:         """Serializa evidencia de contradicción para output"""
>>> 1128:         return {
    1129:             "statement_1": contradiction.statement_a.text,
    1130:             "statement_2": contradiction.statement_b.text,
```

#### Line 1329 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'weights' assigned inline dict literal*

```python
    1327:     def _get_domain_weight(self, dimension: PolicyDimension) -> float:
    1328:         """Obtiene peso específico del dominio"""
>>> 1329:         weights = {
    1330:             PolicyDimension.DIAGNOSTICO: ParameterLoaderV2.get("farfan_core.analysis.contradiction_deteccion.PolicyContradictionDetector._get_domain_weight", "auto_param_L1330_41", 0.8),
    1331:             PolicyDimension.ESTRATEGICO: 1.2,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/derek_beach.py

**54 violation(s)**

#### Line 84 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yaml"*

```python
      82: # CONSTANTS
      83: # ============================================================================
>>>   84: DEFAULT_CONFIG_FILE = "config.yaml"
      85: EXTRACTION_REPORT_SUFFIX = "_extraction_confidence_report.json"
      86: CAUSAL_MODEL_SUFFIX = "_causal_model.json"
```

#### Line 470 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: bayesian_thresholds, mechanism_type_priors*

```python
     468:     def _load_default_config(self) -> None:
     469:         """Load default configuration if custom fails"""
>>>  470:         self.config = {
     471:             'patterns': {
     472:                 'section_titles': r'^(?:CAPÍTULO|ARTÍCULO|PARTE)\s+[\dIVX]+',
```

#### Line 523 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: prior_alpha, prior_beta*

```python
     521:             },
     522:             # Bayesian thresholds - now externalized
>>>  523:             'bayesian_thresholds': {
     524:                 'kl_divergence': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.ConfigLoader._load_default_config", "kl_divergence", 0.01),
     525:                 'convergence_min_evidence': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.ConfigLoader._load_default_config", "convergence_min_evidence", 2),
```

#### Line 546 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: enable_prior_learning, feedback_weight, prior_history_path*

```python
     544:             },
     545:             # Self-reflection settings
>>>  546:             'self_reflection': {
     547:                 'enable_prior_learning': False,
     548:                 'feedback_weight': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.ConfigLoader._load_default_config", "feedback_weight", 0.1),
```

#### Line 638 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'initial_priors' assigned inline dict literal*

```python
     636: 
     637:         # Track initial priors for uncertainty measurement
>>>  638:         initial_priors = {}
     639:         for attr in ['administrativo', 'tecnico', 'financiero', 'politico', 'mixto']:
     640:             if hasattr(self.validated_config.mechanism_type_priors, attr):
```

#### Line 699 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'final_priors' assigned inline dict literal*

```python
     697: 
     698:         # Calculate uncertainty reduction for quality criteria
>>>  699:         final_priors = {}
     700:         for attr in ['administrativo', 'tecnico', 'financiero', 'politico', 'mixto']:
     701:             if hasattr(self.validated_config.mechanism_type_priors, attr):
```

#### Line 748 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: mechanism_type_priors*

```python
     746: 
     747:             # Create new record
>>>  748:             history_record = {
     749:                 'mechanism_type_priors': dict(self.config.get('mechanism_type_priors', {})),
     750:                 'timestamp': pd.Timestamp.now().isoformat(),
```

#### Line 872 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: RuntimeError)
                )
                def load_with_retry():
         *

```python
     870:                     DependencyType.PDF_PARSER,
     871:                     operation_name="open_pdf",
>>>  872:                     exceptions=(IOError, OSError, RuntimeError)
     873:                 )
     874:                 def load_with_retry():
```

#### Line 1157 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: type_transition_prior*

```python
    1155: 
    1156:                     # Calculate evidence components
>>> 1157:                     evidence = {
    1158:                         'keyword': keyword,
    1159:                         'logic': logic,
```

#### Line 1242 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: posterior_mean, posterior_std*

```python
    1240:             )
    1241: 
>>> 1242:             self.causal_chains.append({
    1243:                 'source': source,
    1244:                 'target': target,
```

#### Line 1304 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'transition_priors' assigned inline dict literal*

```python
    1302:         # Define transition probabilities based on logical flow
    1303:         # programa → producto → resultado → impacto
>>> 1304:         transition_priors = {
    1305:             ('programa', 'producto'): ParameterLoaderV2.get("farfan_core.analysis.derek_beach.CausalExtractor._calculate_type_transition_prior", "('programa', 'producto')", 0.85),
    1306:             ('producto', 'resultado'): ParameterLoaderV2.get("farfan_core.analysis.derek_beach.CausalExtractor._calculate_type_transition_prior", "('producto', 'resultado')", 0.80),
```

#### Line 1580 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'weights' assigned inline dict literal*

```python
    1578:         """
    1579:         # Weight different evidence types
>>> 1580:         weights = {
    1581:             'semantic_distance': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.CausalExtractor._calculate_composite_likelihood", "semantic_distance_weight", 0.25),
    1582:             'type_transition_prior': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.CausalExtractor._calculate_composite_likelihood", "type_transition_prior_weight", 0.20),
```

#### Line 1580 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: type_transition_prior*

```python
    1578:         """
    1579:         # Weight different evidence types
>>> 1580:         weights = {
    1581:             'semantic_distance': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.CausalExtractor._calculate_composite_likelihood", "semantic_distance_weight", 0.25),
    1582:             'type_transition_prior': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.CausalExtractor._calculate_composite_likelihood", "type_transition_prior_weight", 0.20),
```

#### Line 2060 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score_cutoff=80*

```python
    2058:             nodes.keys(),
    2059:             scorer=fuzz.ratio,
>>> 2060:             score_cutoff=80
    2061:         )
    2062: 
```

#### Line 2110 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'd3_q3_scores' assigned inline dict literal*

```python
    2108:         and prevents false positives from generic or disconnected budget entries.
    2109:         """
>>> 2110:         d3_q3_scores = {}
    2111: 
    2112:         for node_id, node in nodes.items():
```

#### Line 2154 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: necessity_score*

```python
    2152:                 d3_q3_quality = 'aceptable'
    2153: 
>>> 2154:             d3_q3_scores[node_id] = {
    2155:                 'necessity_score': necessity_score,
    2156:                 'd3_q3_quality': d3_q3_quality,
```

#### Line 2170 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: necessity_score:.2*

```python
    2168:                 node.audit_flags.append('budget_not_necessary')
    2169:                 self.logger.warning(
>>> 2170:                     f"D3-Q3: {node_id} may execute without allocated budget (score={necessity_score:.2f})")
    2171:             elif necessity_score >= ParameterLoaderV2.get("farfan_core.analysis.derek_beach.FinancialAuditor._perform_counterfactual_budget_check", "excellent_threshold", 0.85):
    2172:                 node.audit_flags.append('budget_well_traced')
```

#### Line 2173 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: necessity_score:.2*

```python
    2171:             elif necessity_score >= ParameterLoaderV2.get("farfan_core.analysis.derek_beach.FinancialAuditor._perform_counterfactual_budget_check", "excellent_threshold", 0.85):
    2172:                 node.audit_flags.append('budget_well_traced')
>>> 2173:                 self.logger.info(f"D3-Q3: {node_id} has well-traced, necessary budget (score={necessity_score:.2f})")
    2174: 
    2175:         # Store aggregate D3-Q3 metrics
```

#### Line 2176 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: node_scores, average_necessity_score*

```python
    2174: 
    2175:         # Store aggregate D3-Q3 metrics
>>> 2176:         self.d3_q3_analysis = {
    2177:             'node_scores': d3_q3_scores,
    2178:             'total_products_analyzed': len(d3_q3_scores),
```

#### Line 2271 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'best_score' assigned hardcoded value: 0*

```python
    2269: 
    2270:         best_match = None
>>> 2271:         best_score = 0
    2272: 
    2273:         for entry in budget_entries:
```

#### Line 2271 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: best_score = 0*

```python
    2269: 
    2270:         best_match = None
>>> 2271:         best_score = 0
    2272: 
    2273:         for entry in budget_entries:
```

#### Line 2504 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: risk_score*

```python
    2502:             'systemic_risk': layer3_results,
    2503:             'recommendations': recommendations,
>>> 2504:             'summary': {
    2505:                 'total_nodes': len(nodes),
    2506:                 'critical_omissions': sum(1 for r in layer1_results.values()
```

#### Line 2572 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'rare_evidence_priors' assigned inline dict literal*

```python
    2570:         # Load highly specific priors for rare evidence types
    2571:         # D2-Q4: Risk matrices are rare in poor PDMs (high probative value as Smoking Gun)
>>> 2572:         rare_evidence_priors = {
    2573:             'risk_matrix': {
    2574:                 'prior_alpha': 1.5,  # Low alpha = rare occurrence
```

#### Line 2573 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: prior_alpha, prior_beta*

```python
    2571:         # D2-Q4: Risk matrices are rare in poor PDMs (high probative value as Smoking Gun)
    2572:         rare_evidence_priors = {
>>> 2573:             'risk_matrix': {
    2574:                 'prior_alpha': 1.5,  # Low alpha = rare occurrence
    2575:                 'prior_beta': 12.0,  # High beta = high failure rate when absent
```

#### Line 2578 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: prior_alpha, prior_beta*

```python
    2576:                 'keywords': ['matriz de riesgo', 'análisis de riesgo', 'gestión de riesgo', 'riesgos identificados']
    2577:             },
>>> 2578:             'unwanted_effects': {
    2579:                 'prior_alpha': 1.8,  # D5-Q5: Effects analysis is also rare
    2580:                 'prior_beta': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.OperationalizationAuditor._audit_direct_evidence", "unwanted_effects_prior_beta", 10.5),
```

#### Line 2584 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: prior_alpha, prior_beta*

```python
    2582:                              'consecuencias no previstas']
    2583:             },
>>> 2584:             'theory_of_change': {
    2585:                 'prior_alpha': 1.2,
    2586:                 'prior_beta': 15.0,
```

#### Line 2601 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: prior_alpha, prior_beta, posterior_strength*

```python
    2599:                 if any(kw in node_text_lower for kw in prior_config['keywords']):
    2600:                     # Rare evidence found! Strong Smoking Gun
>>> 2601:                     rare_evidence_found[evidence_type] = {
    2602:                         'prior_alpha': prior_config['prior_alpha'],
    2603:                         'prior_beta': prior_config['prior_beta'],
```

#### Line 2771 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'alignment_penalty_applied' assigned hardcoded value: False*

```python
    2769:         # If pdet_alignment ≤ ParameterLoaderV2.get("farfan_core.analysis.derek_beach.OperationalizationAuditor._audit_systemic_risk", "alignment_threshold", 0.60), apply 1.2× multiplier to risk_score
    2770:         # This enforces integration between D4-Q5 (Alineación) and D5-Q4 (Riesgos Sistémicos)
>>> 2771:         alignment_penalty_applied = False
    2772:         alignment_threshold = ParameterLoaderV2.get("farfan_core.analysis.derek_beach.OperationalizationAuditor._audit_systemic_risk", "alignment_threshold", 0.6) # Refactored
    2773:         alignment_multiplier = 1.2
```

#### Line 2773 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'alignment_multiplier' assigned hardcoded value: 1.2*

```python
    2771:         alignment_penalty_applied = False
    2772:         alignment_threshold = ParameterLoaderV2.get("farfan_core.analysis.derek_beach.OperationalizationAuditor._audit_systemic_risk", "alignment_threshold", 0.6) # Refactored
>>> 2773:         alignment_multiplier = 1.2
    2774: 
    2775:         if pdet_alignment is not None and pdet_alignment <= alignment_threshold:
```

#### Line 2778 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'alignment_penalty_applied' assigned hardcoded value: True*

```python
    2776:             original_risk = risk_score
    2777:             risk_score = risk_score * alignment_multiplier
>>> 2778:             alignment_penalty_applied = True
    2779:             self.logger.warning(
    2780:                 f"ALIGNMENT PENALTY (D5-Q4): pdet_alignment={pdet_alignment:.2f} ≤ {alignment_threshold}, "
```

#### Line 2781 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: risk_score:.3*

```python
    2779:             self.logger.warning(
    2780:                 f"ALIGNMENT PENALTY (D5-Q4): pdet_alignment={pdet_alignment:.2f} ≤ {alignment_threshold}, "
>>> 2781:                 f"risk_score escalated from {original_risk:.3f} to {risk_score:.3f} "
    2782:                 f"(multiplier: {alignment_multiplier}×). Dual constraint per Lieberman 2015."
    2783:             )
```

#### Line 2815 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: risk_score, pdet_alignment, alignment_penalty_applied*

```python
    2813:         )
    2814: 
>>> 2815:         return {
    2816:             'risk_score': min(1.0, risk_score),
    2817:             'success_probability': success_probability,
```

#### Line 2869 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
    2867:                 priority = expected_value / effort
    2868: 
>>> 2869:                 remediations.append({
    2870:                     'node_id': node_id,
    2871:                     'omission': omission,
```

#### Line 3101 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_score*

```python
    3099:         gaps = self._detect_gaps(node, observations, uncertainty)
    3100: 
>>> 3101:         return {
    3102:             'mechanism_type': mechanism_type_posterior,
    3103:             'activity_sequence': sequence_posterior,
```

#### Line 3284 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
    3282:         )
    3283: 
>>> 3284:         return {
    3285:             'score': sufficiency_score,
    3286:             'is_sufficient': sufficiency_score >= 0.6,
```

#### Line 3365 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
    3363:         necessity_score = present_components / max_components
    3364: 
>>> 3365:         result = {
    3366:             'score': necessity_score,
    3367:             'is_necessary': is_necessary,
```

#### Line 3564 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'scores' assigned inline dict literal*

```python
    3562: 
    3563:         # Score each mechanism type
>>> 3564:         scores = {}
    3565:         for mech_type, typical_verbs in self.mechanism_sequences.items():
    3566:             score = ParameterLoaderV2.get("farfan_core.analysis.derek_beach.BayesianMechanismInference._classify_mechanism_type", "score", 0.0) # Refactored
```

#### Line 3991 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_score*

```python
    3989:             rigor_distribution[node.rigor_status] += 1
    3990: 
>>> 3991:         report = {
    3992:             "metadata": {
    3993:                 "policy_code": policy_code,
```

#### Line 4048 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'weights' assigned inline dict literal*

```python
    4046:                                  logic: float, ea: float) -> float:
    4047:         """Calculate overall quality score (0-100)"""
>>> 4048:         weights = {'traceability': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.ReportingEngine._calculate_quality_score", "traceability_weight", 0.35), 'financial': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.ReportingEngine._calculate_quality_score", "financial_weight", 0.25), 'logic': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.ReportingEngine._calculate_quality_score", "logic_weight", 0.25), 'ea': ParameterLoaderV2.get("farfan_core.analysis.derek_beach.ReportingEngine._calculate_quality_score", "ea_weight", 0.15)}
    4049:         score = (traceability * weights['traceability'] +
    4050:                  financial * weights['financial'] +
```

#### Line 4497 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score_promedio:.1*

```python
    4495:         lines.append("-" * 100)
    4496:         lines.append(f"Total de Proyectos/Metas Analizados: {total_proyectos}")
>>> 4497:         lines.append(f"Score Promedio de Cumplimiento: {score_promedio:.1f}/100")
    4498:         lines.append("")
    4499:         lines.append("Distribución por Nivel de Cumplimiento:")
```

#### Line 4522 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score_total:.1*

```python
    4520:             lines.append("-" * 100)
    4521:             lines.append(
>>> 4522:                 f"   Score: {resultado.score_total:.1f}/100 | Nivel: {resultado.nivel_cumplimiento.value.upper()}")
    4523: 
    4524:             # Competencies
```

#### Line 4586 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_score*

```python
    4584:             Dictionary with coherence audit results
    4585:         """
>>> 4586:         audit = {
    4587:             'total_nodes': len(nodes),
    4588:             'total_edges': graph.number_of_edges(),
```

#### Line 4608 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: acyclic_score = 1.0*

```python
    4606:         # Calculate coherence score
    4607:         connected_ratio = 1.0 - (len(audit['disconnected_nodes']) / max(len(nodes), 1))
>>> 4608:         acyclic_score = 1.0 if len(audit['cycles']) == 0 else 0.5
    4609:         audit['coherence_score'] = (connected_ratio + acyclic_score) / 2.0
    4610: 
```

#### Line 4816 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alpha, beta*

```python
    4814: 
    4815:         # Calibration params: logit⁻¹(α + β·score)
>>> 4816:         self.calibration = calibration_params or {
    4817:             'alpha': -2.0,  # Intercept
    4818:             'beta': 4.0     # Slope
```

#### Line 4848 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'domain_scores' assigned inline dict literal*

```python
    4846: 
    4847:         # 2. Extraer scores por dominio
>>> 4848:         domain_scores = {
    4849:             'semantic': evidence_dict.get('semantic', {}).get('score', 0.0),
    4850:             'temporal': evidence_dict.get('temporal', {}).get('score', 0.0),
```

#### Line 4885 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: domain_weights, calibration_params, combined_score*

```python
    4883:         p_mechanism = np.clip(p_mechanism, 1e-6, 1 - 1e-6)
    4884: 
>>> 4885:         return {
    4886:             'p_mechanism': float(p_mechanism),
    4887:             'BF_used': bf_used,
```

#### Line 4970 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
    4968:         for domain in ['semantic', 'financial', 'structural']:
    4969:             ablated_evidence = {
>>> 4970:                 domain: evidence_dict.get(domain, {'score': 0.0})
    4971:             }
    4972:             if ablated_evidence[domain].get('score', 0) > 0:
```

#### Line 5073 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: calibration_params, domain_weights*

```python
    5071: 
    5072:         # Config hash
>>> 5073:         config_str = json.dumps({
    5074:             'bf_table_version': self.bf_table.get_version(),
    5075:             'calibration_params': self.calibration,
```

#### Line 5092 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weights_version*

```python
    5090:         trace_completeness = factors_in_trace / max(total_factors, 1)
    5091: 
>>> 5092:         return {
    5093:             'evidence_trace': evidence_trace,
    5094:             'hash_config': config_hash,
```

#### Line 5188 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: brier_score*

```python
    5186:         monotonicity_ok = monotonicity_violations == 0
    5187: 
>>> 5188:         return {
    5189:             'brier_score': float(brier_score),
    5190:             'brier_ok': brier_ok,
```

#### Line 5340 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: type_posterior, coherence_score, entropy_posterior*

```python
    5338:             self.logger.warning(warning)
    5339: 
>>> 5340:         return {
    5341:             'type_posterior': type_posterior,
    5342:             'sequence_mode': sequence_mode,
```

#### Line 6112 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority_monotonic*

```python
    6110:         risk_in_range = 0.0 <= risk_score <= 1.0
    6111: 
>>> 6112:         criteria_met = {
    6113:             'ci95_valid': ci95_valid,
    6114:             'priority_monotonic': priority_monotonic,
```

#### Line 6118 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: risk_score, priority*

```python
    6116:         }
    6117: 
>>> 6118:         return {
    6119:             'risk_components': risk_components,
    6120:             'risk_score': risk_score,
```

#### Line 6269 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yaml*

```python
    6267: 
    6268: Configuración:
>>> 6269:   El framework busca config.yaml en el directorio actual.
    6270:   Use --config-file para especificar una ruta alternativa.
    6271:         """
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/enhance_recommendation_rules.py

**1 violation(s)**

#### Line 289 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold_days_delay*

```python
     287: 
     288:     # Add escalation path
>>>  289:     enhanced['escalation_path'] = {
     290:         "threshold_days_delay": 15,
     291:         "escalate_to": "Secretaría de Planeación",
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/factory.py

**2 violation(s)**

#### Line 137 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yaml"*

```python
     135:         if not base.exists():
     136:             continue
>>>  137:         for pattern in ("*.yaml", "*.yml"):
     138:             for candidate in base.glob(pattern):
     139:                 if not candidate.is_file():
```

#### Line 137 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yml"*

```python
     135:         if not base.exists():
     136:             continue
>>>  137:         for pattern in ("*.yaml", "*.yml"):
     138:             for candidate in base.glob(pattern):
     139:                 if not candidate.is_file():
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/financiero_viabilidad_tablas.py

**14 violation(s)**

#### Line 291 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: RuntimeError(
                "Modelo SpaCy 'es_dep_news_trf' no instalado. "
  *

```python
     289:             self.nlp = load_spacy_model("es_dep_news_trf")
     290:         except OSError:
>>>  291:             raise RuntimeError(
     292:                 "Modelo SpaCy 'es_dep_news_trf' no instalado. "
     293:                 "Ejecuta: python -m spacy download es_dep_news_trf"
```

#### Line 529 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'scores' assigned inline dict literal*

```python
     527:         for table in tables:
     528:             table_text = table.df.to_string().lower()
>>>  529:             scores = {}
     530:             for table_type, keywords in classification_patterns.items():
     531:                 score = sum(1 for kw in keywords if kw in table_text)
```

#### Line 552 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: sustainability_score*

```python
     550:         risk_assessment = self._bayesian_risk_inference(financial_indicators, funding_sources, sustainability)
     551: 
>>>  552:         return {
     553:             'total_budget': sum(ind.amount for ind in financial_indicators),
     554:             'financial_indicators': [self._indicator_to_dict(ind) for ind in financial_indicators],
```

#### Line 743 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: risk_score, posterior_samples*

```python
     741:         print(f" ✓ Riesgo estimado: {risk_mean:.3f} CI95%: {risk_ci}")
     742: 
>>>  743:         return {
     744:             'risk_score': risk_mean,
     745:             'confidence_interval': risk_ci,
```

#### Line 904 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: distance_threshold=1*

```python
     902:         clustering = AgglomerativeClustering(
     903:             n_clusters=None,
>>>  904:             distance_threshold=1 - similarity_threshold,
     905:             metric='cosine',
     906:             linkage='average'
```

#### Line 1384 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'effect_priors' assigned inline dict literal*

```python
    1382:         Referencia: Cinelli et al. (2022) - Sensitivity Analysis for Causal Inference
    1383:         """
>>> 1384:         effect_priors = {
    1385:             ('Infraestructura y adecuación de tierras', 'productividad_agricola'): (ParameterLoaderV2.get("farfan_core.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer._get_prior_effect", "auto_param_L1385_84", 0.35), ParameterLoaderV2.get("farfan_core.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer._get_prior_effect", "auto_param_L1385_90", 0.15)),
    1386:             ('Salud rural', 'mortalidad_infantil'): (-ParameterLoaderV2.get("farfan_core.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer._get_prior_effect", "auto_param_L1386_54", 0.28), ParameterLoaderV2.get("farfan_core.analysis.financiero_viabilidad_tablas.PDETMunicipalPlanAnalyzer._get_prior_effect", "auto_param_L1386_60", 0.12)),
```

#### Line 1417 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: Layer Causal Hierarchy)
    # ==================================================*

```python
    1415: 
    1416:     # ========================================================================
>>> 1417:     # ANÁLISIS CONTRAFACTUAL (Pearl's Three-Layer Causal Hierarchy)
    1418:     # ========================================================================
    1419: 
```

#### Line 1685 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: pdet_alignment*

```python
    1683:         confidence = self._estimate_score_confidence(scores, weights)
    1684: 
>>> 1685:         evidence = {
    1686:             'financial': financial_score,
    1687:             'indicators': indicator_score,
```

#### Line 1694 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: overall_score:.2*

```python
    1692:         }
    1693: 
>>> 1694:         print(f" ✓ Score final: {overall_score:.2f}/10.0")
    1695: 
    1696:         return QualityScore(
```

#### Line 2145 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_score*

```python
    2143: 
    2144:         # 10. Compilación de resultados
>>> 2145:         results = {
    2146:             'metadata': {
    2147:                 'pdf_path': pdf_path,
```

#### Line 2241 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: specificity_score*

```python
    2239:     def _entity_to_dict(self, entity: ResponsibleEntity) -> dict[str, Any]:
    2240:         """Convierte ResponsibleEntity a diccionario"""
>>> 2241:         return {
    2242:             'name': entity.name,
    2243:             'type': entity.entity_type,
```

#### Line 2253 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: posterior_mean*

```python
    2251:     def _effect_to_dict(self, effect: CausalEffect) -> dict[str, Any]:
    2252:         """Convierte CausalEffect a diccionario"""
>>> 2253:         return {
    2254:             'treatment': effect.treatment,
    2255:             'outcome': effect.outcome,
```

#### Line 2279 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: overall_score, pdet_alignment*

```python
    2277:     def _quality_to_dict(self, quality: QualityScore) -> dict[str, Any]:
    2278:         """Convierte QualityScore a diccionario"""
>>> 2279:         return {
    2280:             'overall_score': quality.overall_score,
    2281:             'financial_feasibility': quality.financial_feasibility,
```

#### Line 2340 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
    2338: 
    2339:         for gap in gaps:
>>> 2340:             remediation = {
    2341:                 'gap_type': gap.get('type', 'unknown'),
    2342:                 'priority': 'high' if gap.get('severity') == 'high' else 'medium',
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/macro_prompts.py

**18 violation(s)**

#### Line 23 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: runtime error fixes for defensive programming
from farfan_pipeline.utils.runtime*

```python
      21: from typing import Any
      22: 
>>>   23: # Import runtime error fixes for defensive programming
      24: from farfan_pipeline.utils.runtime_error_fixes import ensure_list_return
      25: from farfan_pipeline.core.parameters import ParameterLoaderV2
```

#### Line 176 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold_used*

```python
     174:             policy_area_coverage=policy_area_coverage,
     175:             critical_dimensions_below_threshold=critical_below_threshold,
>>>  176:             metadata={
     177:                 "missing_clusters": missing_clusters,
     178:                 "threshold_used": self.coverage_threshold,
```

#### Line 188 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'total_weight' assigned hardcoded value: 0.0*

```python
     186:     ) -> float:
     187:         """Calculate weighted average coverage index"""
>>>  188:         total_weight = 0.0
     189:         weighted_sum = 0.0
     190: 
```

#### Line 188 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: total_weight = 0.0*

```python
     186:     ) -> float:
     187:         """Calculate weighted average coverage index"""
>>>  188:         total_weight = 0.0
     189:         weighted_sum = 0.0
     190: 
```

#### Line 189 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'weighted_sum' assigned hardcoded value: 0.0*

```python
     187:         """Calculate weighted average coverage index"""
     188:         total_weight = 0.0
>>>  189:         weighted_sum = 0.0
     190: 
     191:         for dim, coverage in dimension_coverage.items():
```

#### Line 189 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weighted_sum = 0.0*

```python
     187:         """Calculate weighted average coverage index"""
     188:         total_weight = 0.0
>>>  189:         weighted_sum = 0.0
     190: 
     191:         for dim, coverage in dimension_coverage.items():
```

#### Line 340 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: contradiction_threshold, posterior_threshold*

```python
     338:             micro_meso_alignment=micro_meso_alignment,
     339:             meso_macro_alignment=meso_macro_alignment,
>>>  340:             metadata={
     341:                 "total_micro_claims": len(micro_claims),
     342:                 "contradiction_threshold": self.k,
```

#### Line 400 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
     398:             # Flag if threshold exceeded
     399:             if len(contradicting_claims) >= self.k:
>>>  400:                 contradictions.append({
     401:                     "dimension": dimension,
     402:                     "type": "micro_macro_contradiction",
```

#### Line 554 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: total_weight*

```python
     552:             var_global=var_global,
     553:             confidence_interval=ci,
>>>  554:             metadata={
     555:                 "num_clusters": len(meso_posteriors),
     556:                 "total_weight": sum(cluster_weights.values())
```

#### Line 570 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'weighted_sum' assigned hardcoded value: 0.0*

```python
     568:             return 0.5  # Neutral prior
     569: 
>>>  570:         weighted_sum = 0.0
     571:         for cluster, posterior in meso_posteriors.items():
     572:             weight = cluster_weights.get(cluster, 0.0)
```

#### Line 570 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weighted_sum = 0.0*

```python
     568:             return 0.5  # Neutral prior
     569: 
>>>  570:         weighted_sum = 0.0
     571:         for cluster, posterior in meso_posteriors.items():
     572:             weight = cluster_weights.get(cluster, 0.0)
```

#### Line 630 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'weighted_sq_diff' assigned hardcoded value: 0.0*

```python
     628:             return self.default_variance
     629: 
>>>  630:         weighted_sq_diff = 0.0
     631:         for cluster, posterior in meso_posteriors.items():
     632:             weight = cluster_weights.get(cluster, 0.0)
```

#### Line 630 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weighted_sq_diff = 0.0*

```python
     628:             return self.default_variance
     629: 
>>>  630:         weighted_sq_diff = 0.0
     631:         for cluster, posterior in meso_posteriors.items():
     632:             weight = cluster_weights.get(cluster, 0.0)
```

#### Line 652 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'z_score' assigned hardcoded value: 1.96*

```python
     650:         """Calculate confidence interval (assumes normal distribution)"""
     651:         # For 95% CI, z-score ≈ 1.96
>>>  652:         z_score = 1.96
     653:         margin = z_score * (variance ** 0.5)
     654: 
```

#### Line 652 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: z_score = 1.96*

```python
     650:         """Calculate confidence interval (assumes normal distribution)"""
     651:         # For 95% CI, z-score ≈ 1.96
>>>  652:         z_score = 1.96
     653:         margin = z_score * (variance ** 0.5)
     654: 
```

#### Line 758 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority_ratio*

```python
     756:             ratio = impact / max(effort, ParameterLoaderV2.get("farfan_core.analysis.macro_prompts.RoadmapOptimizer.__init__", "auto_param_L756_41", 0.1))
     757: 
>>>  758:             prioritized.append({
     759:                 **gap,
     760:                 "priority_ratio": ratio,
```

#### Line 1026 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: penalty_threshold*

```python
    1024:             peer_position=peer_position,
    1025:             outlier_areas=outlier_areas,
>>> 1026:             metadata={
    1027:                 "num_policy_areas": len(convergence_by_policy_area),
    1028:                 "low_performers": len(low_performers),
```

#### Line 1039 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'z_scores' assigned inline dict literal*

```python
    1037:     ) -> dict[str, float]:
    1038:         """Calculate z-scores for each policy area"""
>>> 1039:         z_scores = {}
    1040: 
    1041:         for area, score in convergence.items():
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/meso_cluster_analysis.py

**4 violation(s)**

#### Line 79 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'weighted_sum' assigned hardcoded value: 0.0*

```python
      77:         return 0.0
      78:     n = len(seq)
>>>   79:     weighted_sum = 0.0
      80:     for i, value in enumerate(seq, start=1):
      81:         weighted_sum += i * value
```

#### Line 79 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weighted_sum = 0.0*

```python
      77:         return 0.0
      78:     n = len(seq)
>>>   79:     weighted_sum = 0.0
      80:     for i, value in enumerate(seq, start=1):
      81:         weighted_sum += i * value
```

#### Line 210 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: entity_misalignment*

```python
     208:     @calibrated_method("farfan_core.analysis.meso_cluster_analysis.MetricViolation.to_flag_dict")
     209:     def to_flag_dict(self) -> dict[str, object]:
>>>  210:         return {
     211:             "metric_id": self.metric_id,
     212:             "unit_mismatch": self.unit_mismatch,
```

#### Line 363 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: prior_meso, posterior_meso*

```python
     361:     posterior_meso = float(prior_meso * penalty_factor)
     362: 
>>>  363:     json_payload = {
     364:         "prior_meso": prior_meso,
     365:         "penalties": {
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/micro_prompts.py

**2 violation(s)**

#### Line 211 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
     209:         for node_id, node in dag.nodes.items():
     210:             if node.timing > self.p95_threshold:
>>>  211:                 anomalies.append({
     212:                     'node_id': node_id,
     213:                     'timing': node.timing,
```

#### Line 434 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: delta_posterior, likelihood, weight*

```python
     432:     def _signal_to_dict(self, signal: Signal) -> dict[str, Any]:
     433:         """Convert Signal to dictionary"""
>>>  434:         return {
     435:             'rank': 0,  # Will be set by caller if needed
     436:             'test_type': signal.test_type,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/recommendation_engine.py

**5 violation(s)**

#### Line 242 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: default_micro_threshold, default_meso_threshold, default_macro_threshold*

```python
     240:         if self.questionnaire_provider is None:
     241:             logger.warning("No questionnaire provider attached, using default thresholds")
>>>  242:             return {
     243:                 'default_micro_threshold': 2.0,
     244:                 'default_meso_threshold': 55.0,
```

#### Line 252 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'thresholds' assigned inline dict literal*

```python
     250: 
     251:         # Extract thresholds from monolith structure
>>>  252:         thresholds = {}
     253:         blocks = questionnaire_data.get('blocks', {})
     254:         micro_questions = blocks.get('micro_questions', [])
```

#### Line 317 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score_key, actual_score, threshold*

```python
     315:                     horizon=rendered['horizon'],
     316:                     verification=rendered['verification'],
>>>  317:                     metadata={
     318:                         'score_key': score_key,
     319:                         'actual_score': scores[score_key],
```

#### Line 449 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score, score_band*

```python
     447:                 horizon=rendered['horizon'],
     448:                 verification=rendered['verification'],
>>>  449:                 metadata={
     450:                     'cluster_id': cluster_id,
     451:                     'score': cluster_score,
```

#### Line 599 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority_micro_gaps*

```python
     597:                 horizon=rendered['horizon'],
     598:                 verification=rendered['verification'],
>>>  599:                 metadata={
     600:                     'macro_band': actual_band,
     601:                     'clusters_below_target': list(actual_clusters),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/report_assembly.py

**13 violation(s)**

#### Line 36 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: runtime if calibration system available
try:
    from farfan_pipeline.core.param*

```python
      34: 
      35: from pydantic import BaseModel, ConfigDict, Field, field_validator
>>>   36: # Calibration parameters - loaded at runtime if calibration system available
      37: try:
      38:     from farfan_pipeline.core.parameters import ParameterLoaderV2
```

#### Line 250 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'min_score' assigned hardcoded value: 0.0*

```python
     248:         """Validate score is within bounds if present."""
     249:         if v is not None:
>>>  250:             min_score = 0.0
     251:             max_score = 1.0
     252:             if not (min_score <= v <= max_score):
```

#### Line 250 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: min_score = 0.0*

```python
     248:         """Validate score is within bounds if present."""
     249:         if v is not None:
>>>  250:             min_score = 0.0
     251:             max_score = 1.0
     252:             if not (min_score <= v <= max_score):
```

#### Line 251 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'max_score' assigned hardcoded value: 1.0*

```python
     249:         if v is not None:
     250:             min_score = 0.0
>>>  251:             max_score = 1.0
     252:             if not (min_score <= v <= max_score):
     253:                 raise ReportValidationError(
```

#### Line 251 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: max_score = 1.0*

```python
     249:         if v is not None:
     250:             min_score = 0.0
>>>  251:             max_score = 1.0
     252:             if not (min_score <= v <= max_score):
     253:                 raise ReportValidationError(
```

#### Line 255 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
     253:                 raise ReportValidationError(
     254:                     f"Score must be in [{min_score}, {max_score}], got {v}",
>>>  255:                     details={'score': v, 'min': min_score, 'max': max_score},
     256:                     stage="question_validation"
     257:                 )
```

#### Line 995 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.4*

```python
     993:         for cid, cluster in report.meso_clusters.items():
     994:             lines.append(f"\n### Cluster {cid}\n")
>>>  995:             lines.append(f"- **Score:** {cluster.adjusted_score:.4f} (Raw: {cluster.raw_meso_score:.4f})\n")
     996:             lines.append(f"- **Penalties:** Total {cluster.total_penalty:.4f} (Dispersion: {cluster.dispersion_penalty:.4f}, Peer: {cluster.peer_penalty:.4f})\n")
     997: 
```

#### Line 995 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: raw_meso_score:.4*

```python
     993:         for cid, cluster in report.meso_clusters.items():
     994:             lines.append(f"\n### Cluster {cid}\n")
>>>  995:             lines.append(f"- **Score:** {cluster.adjusted_score:.4f} (Raw: {cluster.raw_meso_score:.4f})\n")
     996:             lines.append(f"- **Penalties:** Total {cluster.total_penalty:.4f} (Dispersion: {cluster.dispersion_penalty:.4f}, Peer: {cluster.peer_penalty:.4f})\n")
     997: 
```

#### Line 1000 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.4*

```python
     998:         if report.macro_summary:
     999:             lines.append("\n## Macro Summary\n")
>>> 1000:             lines.append(f"- **Overall Score:** {report.macro_summary.adjusted_score:.4f}\n")
    1001:             lines.append(f"- **Contradictions:** {report.macro_summary.contradiction_count}\n")
    1002: 
```

#### Line 1208 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score=0.85*

```python
    1206:         question_global=1,
    1207:         base_slot="slot1",
>>> 1208:         score=0.85
    1209:     )
    1210: 
```

#### Line 1213 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: raw_meso_score=0.8*

```python
    1211:     meso_cluster = MesoCluster(
    1212:         cluster_id="CL01",
>>> 1213:         raw_meso_score=0.8,
    1214:         adjusted_score=0.75,
    1215:         dispersion_penalty=0.05,
```

#### Line 1214 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score=0.75*

```python
    1212:         cluster_id="CL01",
    1213:         raw_meso_score=0.8,
>>> 1214:         adjusted_score=0.75,
    1215:         dispersion_penalty=0.05,
    1216:         peer_penalty=0.0,
```

#### Line 1222 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score=0.7*

```python
    1220:     macro_summary = MacroSummary(
    1221:         overall_posterior=0.75,
>>> 1222:         adjusted_score=0.7,
    1223:         coverage_penalty=0.05,
    1224:         dispersion_penalty=0.0,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/scoring.py

**25 violation(s)**

#### Line 14 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: threshold=0.7*

```python
      12: SCORING MODALITIES (6 types):
      13: ------------------------------
>>>   14: 1. TYPE_A: Count 4 elements and scale to 0-3 (threshold=0.7 ratio)
      15:    - Used when 4 specific policy elements must be present
      16:    - Threshold: 70% of elements must be found to receive partial credit
```

#### Line 16 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: Threshold: 70*

```python
      14: 1. TYPE_A: Count 4 elements and scale to 0-3 (threshold=0.7 ratio)
      15:    - Used when 4 specific policy elements must be present
>>>   16:    - Threshold: 70% of elements must be found to receive partial credit
      17: 
      18: 2. TYPE_B: Count up to 3 elements, each worth 1 point
```

#### Line 22 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: threshold=0.5*

```python
      20:    - Each element contributes equally to the final score
      21: 
>>>   22: 3. TYPE_C: Count 2 elements and scale to 0-3 (threshold=0.5 ratio)
      23:    - Used when 2 critical policy elements must be present
      24:    - Threshold: 50% of elements must be found to receive partial credit
```

#### Line 24 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: Threshold: 50*

```python
      22: 3. TYPE_C: Count 2 elements and scale to 0-3 (threshold=0.5 ratio)
      23:    - Used when 2 critical policy elements must be present
>>>   24:    - Threshold: 50% of elements must be found to receive partial credit
      25: 
      26: 4. TYPE_D: Count 3 elements, weighted [0.4, 0.3, 0.3]
```

#### Line 246 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: Max_score: 3*

```python
     244:         - Aggregation: "presence_threshold"
     245:         - Threshold: ParameterLoaderV2.get("farfan_core.analysis.scoring.MicroQuestionScorer.score_type_a", "auto_param_L245_21", 0.7)
>>>  246:         - Max_score: 3
     247:         - Expected_elements: 4
     248: 
```

#### Line 287 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold, threshold_met, raw_score*

```python
     285:         score = max(ParameterLoaderV2.get("farfan_core.analysis.scoring.MicroQuestionScorer.score_type_a", "auto_param_L285_20", 0.0), min(max_score, score))
     286: 
>>>  287:         details = {
     288:             'modality': 'TYPE_A',
     289:             'elements_found': elements_found,
```

#### Line 298 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     296:         }
     297: 
>>>  298:         self.logger.debug(f"TYPE_A: {elements_found}/{expected} elementos ({ratio:.2f}) → score={score:.2f}")
     299: 
     300:         return score, details
```

#### Line 313 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: Max_score: 3*

```python
     311:         ESPECIFICACIÓN (línea 34574 del monolith):
     312:         - Aggregation: "binary_sum"
>>>  313:         - Max_score: 3
     314:         - Max_elements: 3
     315: 
```

#### Line 343 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: raw_score*

```python
     341:         score = min(score, max_score)
     342: 
>>>  343:         details = {
     344:             'modality': 'TYPE_B',
     345:             'elements_found': elements_found,
```

#### Line 351 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     349:         }
     350: 
>>>  351:         self.logger.debug(f"TYPE_B: {elements_found} elementos → score={score:.2f}")
     352: 
     353:         return score, details
```

#### Line 367 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: Max_score: 3*

```python
     365:         - Aggregation: "presence_threshold"
     366:         - Threshold: ParameterLoaderV2.get("farfan_core.analysis.scoring.MicroQuestionScorer.score_type_c", "auto_param_L366_21", 0.5)
>>>  367:         - Max_score: 3
     368:         - Expected_elements: 2
     369: 
```

#### Line 406 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold, threshold_met, raw_score*

```python
     404:         score = max(ParameterLoaderV2.get("farfan_core.analysis.scoring.MicroQuestionScorer.score_type_c", "auto_param_L404_20", 0.0), min(max_score, score))
     405: 
>>>  406:         details = {
     407:             'modality': 'TYPE_C',
     408:             'elements_found': elements_found,
```

#### Line 417 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     415:         }
     416: 
>>>  417:         self.logger.debug(f"TYPE_C: {elements_found}/{expected} elementos ({ratio:.2f}) → score={score:.2f}")
     418: 
     419:         return score, details
```

#### Line 433 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: Max_score: 3*

```python
     431:         - Aggregation: "weighted_sum"
     432:         - Weights: [ParameterLoaderV2.get("farfan_core.analysis.scoring.MicroQuestionScorer.score_type_d", "auto_param_L432_20", 0.4), ParameterLoaderV2.get("farfan_core.analysis.scoring.MicroQuestionScorer.score_type_d", "auto_param_L432_25", 0.3), ParameterLoaderV2.get("farfan_core.analysis.scoring.MicroQuestionScorer.score_type_d", "auto_param_L432_30", 0.3)]
>>>  433:         - Max_score: 3
     434:         - Expected_elements: 3
     435: 
```

#### Line 481 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weights, weighted_sum, raw_score*

```python
     479:         score = max(ParameterLoaderV2.get("farfan_core.analysis.scoring.MicroQuestionScorer.score_type_d", "auto_param_L479_20", 0.0), min(max_score, score))
     480: 
>>>  481:         details = {
     482:             'modality': 'TYPE_D',
     483:             'elements_found': elements_found,
```

#### Line 491 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weighted_sum:.2*

```python
     489:         }
     490: 
>>>  491:         self.logger.debug(f"TYPE_D: {elements_found}/{expected} elementos, weighted_sum={weighted_sum:.2f} → score={score:.2f}")
     492: 
     493:         return score, details
```

#### Line 491 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     489:         }
     490: 
>>>  491:         self.logger.debug(f"TYPE_D: {elements_found}/{expected} elementos, weighted_sum={weighted_sum:.2f} → score={score:.2f}")
     492: 
     493:         return score, details
```

#### Line 506 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: Max_score: 3*

```python
     504:         ESPECIFICACIÓN (línea 34596 del monolith):
     505:         - Aggregation: "binary_presence"
>>>  506:         - Max_score: 3
     507: 
     508:         LÓGICA:
```

#### Line 535 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: raw_score*

```python
     533:         score = max_score if has_evidence else ParameterLoaderV2.get("farfan_core.analysis.scoring.MicroQuestionScorer.score_type_e", "auto_param_L533_47", 0.0)
     534: 
>>>  535:         details = {
     536:             'modality': 'TYPE_E',
     537:             'has_evidence': has_evidence,
```

#### Line 545 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     543:         }
     544: 
>>>  545:         self.logger.debug(f"TYPE_E: evidencia={'presente' if has_evidence else 'ausente'} → score={score:.2f}")
     546: 
     547:         return score, details
```

#### Line 561 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: Max_score: 3*

```python
     559:         - Aggregation: "normalized_continuous"
     560:         - Normalization: "minmax"
>>>  561:         - Max_score: 3
     562: 
     563:         LÓGICA:
```

#### Line 598 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: raw_score*

```python
     596:         score = normalized_similarity * max_score
     597: 
>>>  598:         details = {
     599:             'modality': 'TYPE_F',
     600:             'semantic_similarity': similarity,
```

#### Line 606 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     604:         }
     605: 
>>>  606:         self.logger.debug(f"TYPE_F: similarity={similarity:.3f} → score={score:.2f}")
     607: 
     608:         return score, details
```

#### Line 679 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: raw_score:.2*

```python
     677: 
     678:         self.logger.info(
>>>  679:             f"✓ {question_id}: score={raw_score:.2f}/3.0 "
     680:             f"({normalized_score:.2%}), nivel={quality_level.value}"
     681:         )
```

#### Line 680 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: normalized_score:.2*

```python
     678:         self.logger.info(
     679:             f"✓ {question_id}: score={raw_score:.2f}/3.0 "
>>>  680:             f"({normalized_score:.2%}), nivel={quality_level.value}"
     681:         )
     682: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/scoring/scoring.py

**21 violation(s)**

#### Line 396 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: raw_score, max_score*

```python
     394:     score = max(min_score, min(max_score, raw_score))
     395: 
>>>  396:     metadata = {
     397:         "element_count": element_count,
     398:         "confidence": confidence,
```

#### Line 405 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     403: 
     404:     logger.info(
>>>  405:         f"TYPE_A score: {score:.2f} "
     406:         f"(elements={element_count}, confidence={confidence:.2f})"
     407:     )
```

#### Line 449 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: raw_score*

```python
     447:     score = max(config.score_range[0], min(config.score_range[1], raw_score))
     448: 
>>>  449:     metadata = {
     450:         "element_count": element_count,
     451:         "completeness": completeness,
```

#### Line 457 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     455: 
     456:     logger.info(
>>>  457:         f"TYPE_B score: {score:.2f} "
     458:         f"(elements={element_count}, completeness={completeness:.2f})"
     459:     )
```

#### Line 501 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_score, raw_score*

```python
     499:     score = max(config.score_range[0], min(config.score_range[1], raw_score))
     500: 
>>>  501:     metadata = {
     502:         "element_count": element_count,
     503:         "coherence_score": coherence_score,
```

#### Line 509 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     507: 
     508:     logger.info(
>>>  509:         f"TYPE_C score: {score:.2f} "
     510:         f"(elements={element_count}, coherence={coherence_score:.2f})"
     511:     )
```

#### Line 510 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: coherence_score:.2*

```python
     508:     logger.info(
     509:         f"TYPE_C score: {score:.2f} "
>>>  510:         f"(elements={element_count}, coherence={coherence_score:.2f})"
     511:     )
     512: 
```

#### Line 556 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: raw_score*

```python
     554:     score = max(config.score_range[0], min(config.score_range[1], raw_score))
     555: 
>>>  556:     metadata = {
     557:         "element_count": element_count,
     558:         "pattern_matches": match_count,
```

#### Line 564 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     562: 
     563:     logger.info(
>>>  564:         f"TYPE_D score: {score:.2f} "
     565:         f"(elements={element_count}, matches={match_count})"
     566:     )
```

#### Line 611 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: raw_score = 3.0*

```python
     609: 
     610:     # Calculate raw score: presence check weighted by traceability
>>>  611:     raw_score = 3.0 * traceability_score if has_elements else ParameterLoaderV2.get("farfan_core.analysis.scoring.scoring.ModalityConfig.validate_evidence", "auto_param_L610_62", 0.0)
     612: 
     613:     # Clamp to valid range
```

#### Line 616 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: raw_score*

```python
     614:     score = max(config.score_range[0], min(config.score_range[1], raw_score))
     615: 
>>>  616:     metadata = {
     617:         "element_count": element_count,
     618:         "traceability": traceability_score,
```

#### Line 624 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     622: 
     623:     logger.info(
>>>  624:         f"TYPE_E score: {score:.2f} "
     625:         f"(elements={element_count}, traceability={traceability_score:.2f})"
     626:     )
```

#### Line 625 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: traceability_score:.2*

```python
     623:     logger.info(
     624:         f"TYPE_E score: {score:.2f} "
>>>  625:         f"(elements={element_count}, traceability={traceability_score:.2f})"
     626:     )
     627: 
```

#### Line 663 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: raw_score = 3.0*

```python
     661: 
     662:     # Calculate raw score: continuous scale weighted by plausibility
>>>  663:     raw_score = 3.0 * plausibility if element_count > 0 else ParameterLoaderV2.get("farfan_core.analysis.scoring.scoring.ModalityConfig.validate_evidence", "auto_param_L662_61", 0.0)
     664: 
     665:     # Clamp to valid range
```

#### Line 668 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: raw_score*

```python
     666:     score = max(config.score_range[0], min(config.score_range[1], raw_score))
     667: 
>>>  668:     metadata = {
     669:         "element_count": element_count,
     670:         "plausibility": plausibility,
```

#### Line 675 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.2*

```python
     673: 
     674:     logger.info(
>>>  675:         f"TYPE_F score: {score:.2f} "
     676:         f"(elements={element_count}, plausibility={plausibility:.2f})"
     677:     )
```

#### Line 682 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'SCORING_FUNCTIONS' assigned inline dict literal*

```python
     680: 
     681: # Scoring function registry
>>>  682: SCORING_FUNCTIONS = {
     683:     ScoringModality.TYPE_A: score_type_a,
     684:     ScoringModality.TYPE_B: score_type_b,
```

#### Line 713 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'thresholds' assigned inline dict literal*

```python
     711:     """
     712:     if thresholds is None:
>>>  713:         thresholds = {
     714:             "EXCELENTE": ParameterLoaderV2.get("farfan_core.analysis.scoring.scoring.ModalityConfig.validate_evidence", "auto_param_L713_25", 0.85),
     715:             "BUENO": ParameterLoaderV2.get("farfan_core.analysis.scoring.scoring.ModalityConfig.validate_evidence", "auto_param_L714_21", 0.70),
```

#### Line 846 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score_range, score_clamped*

```python
     844:         quality_level=quality_level.value,
     845:         evidence_hash=evidence_hash,
>>>  846:         metadata={
     847:             **metadata,
     848:             "score_range": config.score_range,
```

#### Line 856 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: rounded_score:.2*

```python
     854: 
     855:     logger.info(
>>>  856:         f"✓ Scoring complete: score={rounded_score:.2f}, "
     857:         f"normalized={normalized_score:.2f}, quality={quality_level.value}"
     858:     )
```

#### Line 857 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: normalized_score:.2*

```python
     855:     logger.info(
     856:         f"✓ Scoring complete: score={rounded_score:.2f}, "
>>>  857:         f"normalized={normalized_score:.2f}, quality={quality_level.value}"
     858:     )
     859: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/teoria_cambio.py

**4 violation(s)**

#### Line 515 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: power_threshold, convergence_threshold*

```python
     513:         self.graph_type: GraphType = graph_type
     514:         self._rng: random.Random | None = None
>>>  515:         self.config: dict[str, Any] = {
     516:             "default_iterations": 10000,
     517:             "confidence_level": ParameterLoaderV2.get("farfan_core.analysis.teoria_cambio.AdvancedDAGValidator.__init__", "auto_param_L517_32", 0.95),
```

#### Line 657 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: robustness_score=1*

```python
     655:             edge_sensitivity=sensitivity.get("edge_sensitivity", {}),
     656:             node_importance=self._calculate_node_importance(),
>>>  657:             robustness_score=1 / (1 + sensitivity.get("average_sensitivity", 0)),
     658:             reproducible=True,  # La reproducibilidad es por diseño de la semilla
     659:             convergence_achieved=(p_value * (1 - p_value) / iterations)
```

#### Line 1038 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: threshold:.4*

```python
    1036:         icon = "🟢" if status == STATUS_PASSED else "🔴"
    1037:         self.logger.info(
>>> 1038:             f"    {icon} {name}: {value:.4f} {unit} (Límite: {threshold:.4f} {unit}) - {status}"
    1039:         )
    1040:         return metric
```

#### Line 1143 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: robustness_score:.4*

```python
    1141:             f"  - Poder Estadístico: {result.statistical_power:.4f} {'(ADECUADO)' if result.adequate_power else '(INSUFICIENTE)'}"
    1142:         )
>>> 1143:         LOGGER.info(f"  - Score de Robustez Estructural: {result.robustness_score:.4f}")
    1144:         LOGGER.info(f"  - Tiempo de Cómputo: {result.computation_time:.3f}s")
    1145:         LOGGER.info(
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/api/api_server.py

**37 violation(s)**

#### Line 3 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: Layer
========================================================

Provides REST AP*

```python
       1: #!/usr/bin/env python3
       2: """
>>>    3: AtroZ Dashboard API Server - REST API Integration Layer
       4: ========================================================
       5: 
```

#### Line 263 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     261:         # PDET regions from Colombian government definition
     262:         regions = [
>>>  263:             {
     264:                 'id': 'alto-patia',
     265:                 'name': 'ALTO PATÍA Y NORTE DEL CAUCA',
```

#### Line 281 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     279:                 },
     280:                 'connections': ['pacifico-medio', 'sur-tolima'],
>>>  281:                 'indicators': {
     282:                     'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L277_33", 0.72),
     283:                     'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L278_38", 0.68),
```

#### Line 287 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     285:                 }
     286:             },
>>>  287:             {
     288:                 'id': 'arauca',
     289:                 'name': 'ARAUCA',
```

#### Line 305 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     303:                 },
     304:                 'connections': ['catatumbo'],
>>>  305:                 'indicators': {
     306:                     'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L301_33", 0.68),
     307:                     'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L302_38", 0.65),
```

#### Line 311 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     309:                 }
     310:             },
>>>  311:             {
     312:                 'id': 'bajo-cauca',
     313:                 'name': 'BAJO CAUCA Y NORDESTE ANTIOQUEÑO',
```

#### Line 318 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     316:                 'scores': {'overall': 65, 'governance': 62, 'social': 66, 'economic': 64, 'environmental': 68, 'lastUpdated': datetime.now().isoformat()},
     317:                 'connections': ['sur-cordoba', 'sur-bolivar'],
>>>  318:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L313_44", 0.65), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L313_68", 0.62), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L313_84", 0.67)}
     319:             },
     320:             {
```

#### Line 320 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     318:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L313_44", 0.65), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L313_68", 0.62), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L313_84", 0.67)}
     319:             },
>>>  320:             {
     321:                 'id': 'catatumbo',
     322:                 'name': 'CATATUMBO',
```

#### Line 327 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     325:                 'scores': {'overall': 61, 'governance': 58, 'social': 62, 'economic': 60, 'environmental': 64, 'lastUpdated': datetime.now().isoformat()},
     326:                 'connections': ['arauca'],
>>>  327:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L322_44", 0.61), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L322_68", 0.58), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L322_84", 0.63)}
     328:             },
     329:             {
```

#### Line 329 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     327:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L322_44", 0.61), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L322_68", 0.58), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L322_84", 0.63)}
     328:             },
>>>  329:             {
     330:                 'id': 'choco',
     331:                 'name': 'CHOCÓ',
```

#### Line 336 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     334:                 'scores': {'overall': 58, 'governance': 55, 'social': 59, 'economic': 57, 'environmental': 61, 'lastUpdated': datetime.now().isoformat()},
     335:                 'connections': ['uraba', 'pacifico-medio'],
>>>  336:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L331_44", 0.58), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L331_68", 0.55), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L331_84", 0.60)}
     337:             },
     338:             {
```

#### Line 338 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     336:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L331_44", 0.58), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L331_68", 0.55), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L331_84", 0.60)}
     337:             },
>>>  338:             {
     339:                 'id': 'caguan',
     340:                 'name': 'CUENCA DEL CAGUÁN Y PIEDEMONTE CAQUETEÑO',
```

#### Line 345 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     343:                 'scores': {'overall': 70, 'governance': 67, 'social': 71, 'economic': 69, 'environmental': 72, 'lastUpdated': datetime.now().isoformat()},
     344:                 'connections': ['macarena', 'putumayo'],
>>>  345:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L340_44", 0.70), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L340_68", 0.67), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L340_84", 0.71)}
     346:             },
     347:             {
```

#### Line 347 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     345:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L340_44", 0.70), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L340_68", 0.67), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L340_84", 0.71)}
     346:             },
>>>  347:             {
     348:                 'id': 'macarena',
     349:                 'name': 'MACARENA-GUAVIARE',
```

#### Line 354 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     352:                 'scores': {'overall': 66, 'governance': 63, 'social': 67, 'economic': 65, 'environmental': 68, 'lastUpdated': datetime.now().isoformat()},
     353:                 'connections': ['caguan'],
>>>  354:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L349_44", 0.66), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L349_68", 0.63), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L349_84", 0.67)}
     355:             },
     356:             {
```

#### Line 356 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     354:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L349_44", 0.66), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L349_68", 0.63), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L349_84", 0.67)}
     355:             },
>>>  356:             {
     357:                 'id': 'montes-maria',
     358:                 'name': 'MONTES DE MARÍA',
```

#### Line 363 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     361:                 'scores': {'overall': 74, 'governance': 71, 'social': 75, 'economic': 73, 'environmental': 76, 'lastUpdated': datetime.now().isoformat()},
     362:                 'connections': ['sur-bolivar'],
>>>  363:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L358_44", 0.74), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L358_68", 0.71), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L358_84", 0.75)}
     364:             },
     365:             {
```

#### Line 365 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     363:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L358_44", 0.74), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L358_68", 0.71), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L358_84", 0.75)}
     364:             },
>>>  365:             {
     366:                 'id': 'pacifico-medio',
     367:                 'name': 'PACÍFICO MEDIO',
```

#### Line 372 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     370:                 'scores': {'overall': 62, 'governance': 59, 'social': 63, 'economic': 61, 'environmental': 64, 'lastUpdated': datetime.now().isoformat()},
     371:                 'connections': ['choco', 'alto-patia'],
>>>  372:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L367_44", 0.62), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L367_68", 0.59), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L367_84", 0.63)}
     373:             },
     374:             {
```

#### Line 374 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     372:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L367_44", 0.62), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L367_68", 0.59), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L367_84", 0.63)}
     373:             },
>>>  374:             {
     375:                 'id': 'pacifico-narinense',
     376:                 'name': 'PACÍFICO Y FRONTERA NARIÑENSE',
```

#### Line 381 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     379:                 'scores': {'overall': 59, 'governance': 56, 'social': 60, 'economic': 58, 'environmental': 61, 'lastUpdated': datetime.now().isoformat()},
     380:                 'connections': ['putumayo'],
>>>  381:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L376_44", 0.59), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L376_68", 0.56), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L376_84", 0.60)}
     382:             },
     383:             {
```

#### Line 383 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     381:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L376_44", 0.59), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L376_68", 0.56), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L376_84", 0.60)}
     382:             },
>>>  383:             {
     384:                 'id': 'putumayo',
     385:                 'name': 'PUTUMAYO',
```

#### Line 390 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     388:                 'scores': {'overall': 67, 'governance': 64, 'social': 68, 'economic': 66, 'environmental': 69, 'lastUpdated': datetime.now().isoformat()},
     389:                 'connections': ['caguan', 'pacifico-narinense'],
>>>  390:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L385_44", 0.67), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L385_68", 0.64), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L385_84", 0.68)}
     391:             },
     392:             {
```

#### Line 392 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     390:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L385_44", 0.67), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L385_68", 0.64), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L385_84", 0.68)}
     391:             },
>>>  392:             {
     393:                 'id': 'sierra-nevada',
     394:                 'name': 'SIERRA NEVADA - PERIJÁ - ZONA BANANERA',
```

#### Line 399 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     397:                 'scores': {'overall': 63, 'governance': 60, 'social': 64, 'economic': 62, 'environmental': 65, 'lastUpdated': datetime.now().isoformat()},
     398:                 'connections': ['catatumbo'],
>>>  399:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L394_44", 0.63), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L394_68", 0.60), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L394_84", 0.64)}
     400:             },
     401:             {
```

#### Line 401 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     399:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L394_44", 0.63), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L394_68", 0.60), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L394_84", 0.64)}
     400:             },
>>>  401:             {
     402:                 'id': 'sur-bolivar',
     403:                 'name': 'SUR DE BOLÍVAR',
```

#### Line 408 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     406:                 'scores': {'overall': 60, 'governance': 57, 'social': 61, 'economic': 59, 'environmental': 62, 'lastUpdated': datetime.now().isoformat()},
     407:                 'connections': ['bajo-cauca', 'montes-maria'],
>>>  408:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L403_44", 0.60), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L403_68", 0.57), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L403_84", 0.61)}
     409:             },
     410:             {
```

#### Line 410 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     408:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L403_44", 0.60), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L403_68", 0.57), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L403_84", 0.61)}
     409:             },
>>>  410:             {
     411:                 'id': 'sur-cordoba',
     412:                 'name': 'SUR DE CÓRDOBA',
```

#### Line 417 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     415:                 'scores': {'overall': 69, 'governance': 66, 'social': 70, 'economic': 68, 'environmental': 71, 'lastUpdated': datetime.now().isoformat()},
     416:                 'connections': ['bajo-cauca', 'uraba'],
>>>  417:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L412_44", 0.69), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L412_68", 0.66), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L412_84", 0.70)}
     418:             },
     419:             {
```

#### Line 419 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     417:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L412_44", 0.69), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L412_68", 0.66), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L412_84", 0.70)}
     418:             },
>>>  419:             {
     420:                 'id': 'sur-tolima',
     421:                 'name': 'SUR DEL TOLIMA',
```

#### Line 426 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     424:                 'scores': {'overall': 71, 'governance': 68, 'social': 72, 'economic': 70, 'environmental': 73, 'lastUpdated': datetime.now().isoformat()},
     425:                 'connections': ['alto-patia', 'caguan'],
>>>  426:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L421_44", 0.71), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L421_68", 0.68), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L421_84", 0.72)}
     427:             },
     428:             {
```

#### Line 428 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: scores*

```python
     426:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L421_44", 0.71), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L421_68", 0.68), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L421_84", 0.72)}
     427:             },
>>>  428:             {
     429:                 'id': 'uraba',
     430:                 'name': 'URABÁ ANTIOQUEÑO',
```

#### Line 435 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alignment*

```python
     433:                 'scores': {'overall': 64, 'governance': 61, 'social': 65, 'economic': 63, 'environmental': 66, 'lastUpdated': datetime.now().isoformat()},
     434:                 'connections': ['choco', 'sur-cordoba'],
>>>  435:                 'indicators': {'alignment': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L430_44", 0.64), 'implementation': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L430_68", 0.61), 'impact': ParameterLoaderV2.get("farfan_core.api.api_server.DataService.get_pdet_regions", "auto_param_L430_84", 0.65)}
     436:             }
     437:         ]
```

#### Line 500 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
     498:         for i in range(1, 45):
     499:             score = random.uniform(ParameterLoaderV2.get("farfan_core.api.api_server.DataService._get_question_matrix", "auto_param_L468_35", 0.4), ParameterLoaderV2.get("farfan_core.api.api_server.DataService._get_question_matrix", "auto_param_L468_40", 1.0))
>>>  500:             questions.append({
     501:                 'id': i,
     502:                 'text': f'Pregunta {i}',
```

#### Line 514 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
     512:         """Get strategic recommendations for region"""
     513:         return [
>>>  514:             {
     515:                 'priority': 'ALTA',
     516:                 'text': 'Fortalecer mecanismos de participación ciudadana',
```

#### Line 520 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
     518:                 'impact': 'HIGH'
     519:             },
>>>  520:             {
     521:                 'priority': 'ALTA',
     522:                 'text': 'Implementar sistema de monitoreo continuo',
```

#### Line 526 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
     524:                 'impact': 'HIGH'
     525:             },
>>>  526:             {
     527:                 'priority': 'MEDIA',
     528:                 'text': 'Mejorar articulación interinstitucional',
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/contracts/retriever_contract.py

**1 violation(s)**

#### Line 25 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      23:         for i in range(top_k):
      24:             doc_hash = hashlib.blake2b(f"{current_hash}:{i}".encode()).hexdigest()
>>>   25:             results.append({
      26:                 "id": f"doc_{doc_hash[:8]}",
      27:                 "score": 0.9 - (i * 0.1),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/contracts/risk_certificate.py

**1 violation(s)**

#### Line 44 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alpha, threshold*

```python
      42:         risk = 1.0 - coverage
      43: 
>>>   44:         return {
      45:             "alpha": alpha,
      46:             "threshold": float(threshold),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/contracts/tests/test_rcc.py

**2 violation(s)**

#### Line 15 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'alpha' assigned hardcoded value: 0.1*

```python
      13:         cal_data = [0.1, 0.2, 0.5, 0.8]
      14:         holdout = [0.15, 0.6]
>>>   15:         alpha = 0.1
      16:         seed = 42
      17: 
```

#### Line 30 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'alpha' assigned hardcoded value: 0.1*

```python
      28:         cal_data = list(data[:800])
      29:         holdout = list(data[800:])
>>>   30:         alpha = 0.1
      31: 
      32:         res = RiskCertificateContract.verify_risk(cal_data, holdout, alpha, 42)
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/contracts/tests/test_refusal.py

**2 violation(s)**

#### Line 19 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alpha*

```python
      17:         # Alpha violation
      18:         with pytest.raises(RefusalError, match="Alpha violation"):
>>>   19:             RefusalContract.check_prerequisites({"mandatory": True, "alpha": 0.8})
      20: 
      21:         # Sigma absent
```

#### Line 23 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alpha*

```python
      21:         # Sigma absent
      22:         with pytest.raises(RefusalError, match="Sigma absent"):
>>>   23:             RefusalContract.check_prerequisites({"mandatory": True, "alpha": 0.1})
      24: 
      25: if __name__ == "__main__":
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/contracts/tests/test_toc.py

**5 violation(s)**

#### Line 13 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      11:         """Casos de empate sintéticos: mismo score_vector ⇒ desempate por κ.lexicográfico."""
      12:         items = [
>>>   13:             {"score": 10, "content_hash": "b"},
      14:             {"score": 10, "content_hash": "a"},
      15:             {"score": 5, "content_hash": "c"}
```

#### Line 14 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      12:         items = [
      13:             {"score": 10, "content_hash": "b"},
>>>   14:             {"score": 10, "content_hash": "a"},
      15:             {"score": 5, "content_hash": "c"}
      16:         ]
```

#### Line 15 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      13:             {"score": 10, "content_hash": "b"},
      14:             {"score": 10, "content_hash": "a"},
>>>   15:             {"score": 5, "content_hash": "c"}
      16:         ]
      17: 
```

#### Line 28 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      26:     def test_stability(self):
      27:         items = [
>>>   28:             {"score": 10, "content_hash": "b"},
      29:             {"score": 10, "content_hash": "a"}
      30:         ]
```

#### Line 29 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      27:         items = [
      28:             {"score": 10, "content_hash": "b"},
>>>   29:             {"score": 10, "content_hash": "a"}
      30:         ]
      31:         assert TotalOrderingContract.verify_order(items, lambda x: x["score"])
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/contracts/tools/rcc_report.py

**2 violation(s)**

#### Line 15 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'alpha' assigned hardcoded value: 0.05*

```python
      13:     cal_data = list(np.random.beta(2, 5, 500))
      14:     holdout_data = list(np.random.beta(2, 5, 200))
>>>   15:     alpha = 0.05
      16:     seed = 123
      17: 
```

#### Line 25 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alpha*

```python
      23:     print(f"Risk: {result['risk']:.4f}")
      24: 
>>>   25:     certificate = {
      26:         "pass": True,
      27:         "alpha": result['alpha'],
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/contracts/tools/refusal_matrix.py

**3 violation(s)**

#### Line 11 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alpha*

```python
       9: def main():
      10:     scenarios = [
>>>   11:         {"name": "Valid", "ctx": {"mandatory": True, "alpha": 0.1, "sigma": "ok"}},
      12:         {"name": "No Mandatory", "ctx": {"alpha": 0.1}},
      13:         {"name": "Bad Alpha", "ctx": {"mandatory": True, "alpha": 0.9}},
```

#### Line 12 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alpha*

```python
      10:     scenarios = [
      11:         {"name": "Valid", "ctx": {"mandatory": True, "alpha": 0.1, "sigma": "ok"}},
>>>   12:         {"name": "No Mandatory", "ctx": {"alpha": 0.1}},
      13:         {"name": "Bad Alpha", "ctx": {"mandatory": True, "alpha": 0.9}},
      14:     ]
```

#### Line 13 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alpha*

```python
      11:         {"name": "Valid", "ctx": {"mandatory": True, "alpha": 0.1, "sigma": "ok"}},
      12:         {"name": "No Mandatory", "ctx": {"alpha": 0.1}},
>>>   13:         {"name": "Bad Alpha", "ctx": {"mandatory": True, "alpha": 0.9}},
      14:     ]
      15: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/contracts/tools/sort_sanity.py

**3 violation(s)**

#### Line 11 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
       9: def main():
      10:     items = [
>>>   11:         {"id": 1, "score": 0.5, "content_hash": "z"},
      12:         {"id": 2, "score": 0.5, "content_hash": "a"},
      13:         {"id": 3, "score": 0.8, "content_hash": "m"}
```

#### Line 12 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      10:     items = [
      11:         {"id": 1, "score": 0.5, "content_hash": "z"},
>>>   12:         {"id": 2, "score": 0.5, "content_hash": "a"},
      13:         {"id": 3, "score": 0.8, "content_hash": "m"}
      14:     ]
```

#### Line 13 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      11:         {"id": 1, "score": 0.5, "content_hash": "z"},
      12:         {"id": 2, "score": 0.5, "content_hash": "a"},
>>>   13:         {"id": 3, "score": 0.8, "content_hash": "m"}
      14:     ]
      15: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/calibration_registry.py

**5 violation(s)**

#### Line 92 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable '_calibration_cache' assigned inline dict literal*

```python
      90:     if not _CALIBRATION_FILE.exists():
      91:         logger.warning(f"Calibration file not found: {_CALIBRATION_FILE}")
>>>   92:         _calibration_cache = {}
      93:         return _calibration_cache
      94: 
```

#### Line 103 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable '_calibration_cache' assigned inline dict literal*

```python
     101:     except Exception as e:
     102:         logger.error(f"Failed to load calibration data: {e}")
>>>  103:         _calibration_cache = {}
     104:         return _calibration_cache
     105: 
```

#### Line 114 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score_min=0.0*

```python
     112:     """
     113:     return MethodCalibration(
>>>  114:         score_min=0.0,
     115:         score_max=1.0,
     116:         min_evidence_snippets=3,
```

#### Line 115 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score_max=1.0*

```python
     113:     return MethodCalibration(
     114:         score_min=0.0,
>>>  115:         score_max=1.0,
     116:         min_evidence_snippets=3,
     117:         max_evidence_snippets=15,
```

#### Line 120 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: aggregation_weight=1.0*

```python
     118:         contradiction_tolerance=0.1,
     119:         uncertainty_penalty=0.3,
>>>  120:         aggregation_weight=1.0,
     121:         sensitivity=0.75,
     122:         requires_numeric_support=False,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/chain_layer.py

**3 violation(s)**

#### Line 2 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: Layer (@chain) - Full Implementation.

Validates data flow integrity for method *

```python
       1: """
>>>    2: Chain Layer (@chain) - Full Implementation.
       3: 
       4: Validates data flow integrity for method chains.
```

#### Line 114 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
     112: 
     113:         # All inputs present
>>>  114:         logger.info("chain_valid", extra={"method": method_id, "score": 1.0})
     115:         return 1.0
     116: 
```

#### Line 166 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: min_score*

```python
     164:         logger.info(
     165:             "chain_quality_computed",
>>>  166:             extra={
     167:                 "min_score": min_score,
     168:                 "num_methods": len(method_scores)
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/choquet_aggregator.py

**11 violation(s)**

#### Line 8 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: layer scores)
- Second sum: interaction terms (synergies via weakest link)
"""
i*

```python
       6: 
       7: Where:
>>>    8: - First sum: linear terms (weighted sum of layer scores)
       9: - Second sum: interaction terms (synergies via weakest link)
      10: """
```

#### Line 43 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: num_layers*

```python
      41:         logger.info(
      42:             "choquet_aggregator_initialized",
>>>   43:             extra={
      44:                 "num_layers": len(self.config.linear_weights),
      45:                 "num_interactions": len(self.interaction_terms),
```

#### Line 90 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score = 0.0*

```python
      88:                 }
      89:             )
>>>   90:             # For missing layers, use score = 0.0
      91:             for layer in missing_layers:
      92:                 scores[layer] = 0.0
```

#### Line 108 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layer, weight, score*

```python
     106:             logger.debug(
     107:                 "linear_term",
>>>  108:                 extra={
     109:                     "layer": layer_key,
     110:                     "weight": weight,
```

#### Line 133 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: layer_1.value}_{term.layer_2.value}"
            interaction_breakdown[key] = {
*

```python
     131:             interaction_contribution += contribution
     132: 
>>>  133:             key = f"{term.layer_1.value}_{term.layer_2.value}"
     134:             interaction_breakdown[key] = {
     135:                 "contribution": contribution,
```

#### Line 134 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight, score_1, score_2*

```python
     132: 
     133:             key = f"{term.layer_1.value}_{term.layer_2.value}"
>>>  134:             interaction_breakdown[key] = {
     135:                 "contribution": contribution,
     136:                 "weight": term.weight,
```

#### Line 148 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layers, weight, min_score*

```python
     146:             logger.debug(
     147:                 "interaction_term",
>>>  148:                 extra={
     149:                     "layers": f"{term.layer_1.value}+{term.layer_2.value}",
     150:                     "weight": term.weight,
```

#### Line 149 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: layers": f"{term.layer_1.value}+{term.layer_2.value}",
                    "weig*

```python
     147:                 "interaction_term",
     148:                 extra={
>>>  149:                     "layers": f"{term.layer_1.value}+{term.layer_2.value}",
     150:                     "weight": term.weight,
     151:                     "min_score": interaction_breakdown[key]["min_score"],
```

#### Line 173 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: final_score*

```python
     171:             logger.error(
     172:                 "final_score_out_of_bounds",
>>>  173:                 extra={
     174:                     "final_score": final_score,
     175:                     "linear_contribution": linear_contribution,
```

#### Line 181 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: final_score:.6*

```python
     179:             )
     180:             raise ValueError(
>>>  181:                 f"Final score {final_score:.6f} out of bounds [0.0, 1.0]. "
     182:                 f"This indicates a bug in weight normalization or layer score validation."
     183:             )
```

#### Line 187 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: final_score*

```python
     185:         logger.info(
     186:             "final_calibration_computed",
>>>  187:             extra={
     188:                 "method": subject.method_id,
     189:                 "context": f"{subject.context.question_id}_{subject.context.dimension}_{subject.context.policy_area}",
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/compatibility.py

**5 violation(s)**

#### Line 92 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: default_score*

```python
      90:             logger.warning(
      91:                 "method_compatibility_not_found",
>>>   92:                 extra={
      93:                     "method": method_id,
      94:                     "default_score": 0.1
```

#### Line 145 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: LayerEvaluator:
    """
    Evaluates the three contextual layers: @q, @d, @p.
 *

```python
     143: 
     144: 
>>>  145: class ContextualLayerEvaluator:
     146:     """
     147:     Evaluates the three contextual layers: @q, @d, @p.
```

#### Line 166 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
     164:         logger.debug(
     165:             "question_compatibility",
>>>  166:             extra={
     167:                 "method": method_id,
     168:                 "question": question_id,
```

#### Line 186 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
     184:         logger.debug(
     185:             "dimension_compatibility",
>>>  186:             extra={
     187:                 "method": method_id,
     188:                 "dimension": dimension,
```

#### Line 206 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
     204:         logger.debug(
     205:             "policy_compatibility",
>>>  206:             extra={
     207:                 "method": method_id,
     208:                 "policy": policy_area,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/config 2.py

**8 violation(s)**

#### Line 265 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score = 0.0*

```python
     263:     threshold_acceptable: float = 5.0  # Acceptable performance
     264:     # If runtime > threshold_acceptable → score drops to 0.5
>>>  265:     # If timeout or out_of_memory → score = 0.0
     266: 
     267:     # Memory thresholds (MB)
```

#### Line 430 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: choquet*

```python
     428:         proves which configuration was used.
     429:         """
>>>  430:         config_dict = {
     431:             "unit": {
     432:                 "weights": [self.unit_layer.w_S, self.unit_layer.w_M,
```

#### Line 431 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weights*

```python
     429:         """
     430:         config_dict = {
>>>  431:             "unit": {
     432:                 "weights": [self.unit_layer.w_S, self.unit_layer.w_M,
     433:                            self.unit_layer.w_I, self.unit_layer.w_P],
```

#### Line 443 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weights*

```python
     441:                 }
     442:             },
>>>  443:             "meta": {
     444:                 "weights": [self.meta_layer.w_transparency,
     445:                            self.meta_layer.w_governance,
```

#### Line 459 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: unit_layer, meta_layer, choquet*

```python
     457:     def to_dict(self) -> dict:
     458:         """Export configuration as dictionary."""
>>>  459:         return {
     460:             "system_hash": self.compute_system_hash(),
     461:             "unit_layer": {
```

#### Line 461 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weights*

```python
     459:         return {
     460:             "system_hash": self.compute_system_hash(),
>>>  461:             "unit_layer": {
     462:                 "weights": {
     463:                     "S": self.unit_layer.w_S,
```

#### Line 475 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weights*

```python
     473:                 }
     474:             },
>>>  475:             "meta_layer": {
     476:                 "weights": {
     477:                     "transparency": self.meta_layer.w_transparency,
```

#### Line 482 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: linear_weights*

```python
     480:                 }
     481:             },
>>>  482:             "choquet": {
     483:                 "linear_weights": self.choquet.linear_weights,
     484:                 "interaction_count": len(self.choquet.interaction_weights),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/congruence_layer.py

**6 violation(s)**

#### Line 2 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: Layer (@C) - Full Implementation.

Evaluates method ensemble congruence using th*

```python
       1: """
>>>    2: Congruence Layer (@C) - Full Implementation.
       3: 
       4: Evaluates method ensemble congruence using three components:
```

#### Line 60 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      58:             method_id = method_ids[0] if method_ids else None
      59:             if method_id is not None and method_id in self.registry:
>>>   60:                 logger.debug("congruence_single_method", extra={"score": 1.0, "method_id": method_id})
      61:                 return 1.0
      62:             else:
```

#### Line 63 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      61:                 return 1.0
      62:             else:
>>>   63:                 logger.warning("congruence_single_method_missing", extra={"score": 0.0, "method_id": method_id})
      64:                 return 0.0
      65: 
```

#### Line 77 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      75:         # Component 1: Scale congruence (c_scale)
      76:         c_scale = self._compute_scale_congruence(method_ids)
>>>   77:         logger.debug("c_scale_computed", extra={"score": c_scale})
      78: 
      79:         # Component 2: Semantic congruence (c_sem)
```

#### Line 81 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      79:         # Component 2: Semantic congruence (c_sem)
      80:         c_sem = self._compute_semantic_congruence(method_ids)
>>>   81:         logger.debug("c_sem_computed", extra={"score": c_sem})
      82: 
      83:         # Component 3: Fusion validity (c_fusion)
```

#### Line 87 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      85:             method_ids, fusion_rule, provided_inputs or []
      86:         )
>>>   87:         logger.debug("c_fusion_computed", extra={"score": c_fusion})
      88: 
      89:         # Final score: Product of three components
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/data_structures-2.py

**15 violation(s)**

#### Line 18 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: LayerID(str, Enum):
    """
    Exact identifier for each calibration layer.
   *

```python
      16: 
      17: 
>>>   18: class LayerID(str, Enum):
      19:     """
      20:     Exact identifier for each calibration layer.
```

#### Line 51 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score=0.75*

```python
      49:         LayerScore(
      50:             layer=LayerID.UNIT,
>>>   51:             score=0.75,
      52:             components={"S": 0.8, "M": 0.7, "I": 0.75, "P": 0.75},
      53:             rationale="Unit quality: robusto (S=0.80, M=0.70, I=0.75, P=0.75)",
```

#### Line 72 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layer, score*

```python
      70:     def to_dict(self) -> dict:
      71:         """Export as dictionary for JSON serialization."""
>>>   72:         return {
      73:             "layer": self.layer.value,
      74:             "score": self.score,
```

#### Line 278 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: layers in Choquet aggregation.
    
    Formula: a_ℓk · min(x_ℓ, x_k)
    
    T*

```python
     276: class InteractionTerm:
     277:     """
>>>  278:     Represents a synergy between two layers in Choquet aggregation.
     279: 
     280:     Formula: a_ℓk · min(x_ℓ, x_k)
```

#### Line 286 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight=0.15*

```python
     284: 
     285:     Standard Interactions (from theoretical model):
>>>  286:         (@u, @chain): weight=0.15, "Plan quality only matters with sound wiring"
     287:         (@chain, @C): weight=0.12, "Ensemble validity requires chain integrity"
     288:         (@q, @d): weight=0.08, "Question-dimension alignment synergy"
```

#### Line 287 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight=0.12*

```python
     285:     Standard Interactions (from theoretical model):
     286:         (@u, @chain): weight=0.15, "Plan quality only matters with sound wiring"
>>>  287:         (@chain, @C): weight=0.12, "Ensemble validity requires chain integrity"
     288:         (@q, @d): weight=0.08, "Question-dimension alignment synergy"
     289:         (@d, @p): weight=0.05, "Dimension-policy coherence synergy"
```

#### Line 288 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight=0.08*

```python
     286:         (@u, @chain): weight=0.15, "Plan quality only matters with sound wiring"
     287:         (@chain, @C): weight=0.12, "Ensemble validity requires chain integrity"
>>>  288:         (@q, @d): weight=0.08, "Question-dimension alignment synergy"
     289:         (@d, @p): weight=0.05, "Dimension-policy coherence synergy"
     290: 
```

#### Line 289 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight=0.05*

```python
     287:         (@chain, @C): weight=0.12, "Ensemble validity requires chain integrity"
     288:         (@q, @d): weight=0.08, "Question-dimension alignment synergy"
>>>  289:         (@d, @p): weight=0.05, "Dimension-policy coherence synergy"
     290: 
     291:     Example:
```

#### Line 295 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight=0.15*

```python
     293:             layer_1=LayerID.UNIT,
     294:             layer_2=LayerID.CHAIN,
>>>  295:             weight=0.15,
     296:             rationale="Plan quality only matters with sound wiring"
     297:         )
```

#### Line 322 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layer_1, layer_2, weight*

```python
     320:     def to_dict(self) -> dict:
     321:         """Export as dictionary."""
>>>  322:         return {
     323:             "layer_1": self.layer_1.value,
     324:             "layer_2": self.layer_2.value,
```

#### Line 351 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score=0.9*

```python
     349:             subject=CalibrationSubject(...),
     350:             layer_scores={
>>>  351:                 LayerID.BASE: LayerScore(..., score=0.9),
     352:                 LayerID.UNIT: LayerScore(..., score=0.75),
     353:                 ...
```

#### Line 352 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score=0.75*

```python
     350:             layer_scores={
     351:                 LayerID.BASE: LayerScore(..., score=0.9),
>>>  352:                 LayerID.UNIT: LayerScore(..., score=0.75),
     353:                 ...
     354:             },
```

#### Line 357 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: final_score=0.80*

```python
     355:             linear_contribution=0.65,
     356:             interaction_contribution=0.15,
>>>  357:             final_score=0.80,
     358:             computation_metadata={
     359:                 "config_hash": "abc123",
```

#### Line 402 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layer_scores*

```python
     400:         used to reproduce the calibration result.
     401:         """
>>>  402:         return {
     403:             "certificate_version": "1.0",
     404:             "method": {
```

#### Line 415 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: final_score*

```python
     413:                 for layer_id, layer_score in self.layer_scores.items()
     414:             },
>>>  415:             "aggregation": {
     416:                 "linear_contribution": self.linear_contribution,
     417:                 "interaction_contribution": self.interaction_contribution,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/engine.py

**14 violation(s)**

#### Line 7 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: Runtime Engine)
SIN_CARRETA Compliance: Pure fusion operator, fail-loudly on mis*

```python
       5: as specified in the SUPERPROMPT Three-Pillar Calibration System.
       6: 
>>>    7: Spec compliance: Section 5 (Fusion Operator), Section 6 (Runtime Engine)
       8: SIN_CARRETA Compliance: Pure fusion operator, fail-loudly on misconfiguration
       9: """
```

#### Line 114 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layer*

```python
     112:                 for key in [canonical_name, method_name, f"{class_name}.{method_name}"]:
     113:                     if key:
>>>  114:                         self.method_index[key] = {
     115:                             "canonical_name": canonical_name,
     116:                             "method_name": method_name,
```

#### Line 162 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: total_weight:.15*

```python
     160:                 raise CalibrationConfigError(
     161:                     f"Weight sum must equal 1.0 for role={role_name}: "
>>>  162:                     f"total_weight={total_weight:.15f} (deviation: {abs(total_weight - 1.0):.15f}). "
     163:                     f"Constraint: Σ(a_ℓ) + Σ(a_ℓk) = 1.0 (tolerance {TOLERANCE})."
     164:                 )
```

#### Line 307 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: layer_scores(
        self, 
        subject: CalibrationSubject,
        eviden*

```python
     305:         return None
     306: 
>>>  307:     def _compute_layer_scores(
     308:         self,
     309:         subject: CalibrationSubject,
```

#### Line 318 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'scores' assigned inline dict literal*

```python
     316:         """
     317:         ctx = subject.context
>>>  318:         scores = {}
     319: 
     320:         # @b: Base layer (always required)
```

#### Line 357 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: runtime_ms*

```python
     355: 
     356:         # @m: Meta/governance
>>>  357:         meta_evidence = {
     358:             "formula_export_valid": True,
     359:             "trace_complete": True,
```

#### Line 411 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layer, weight, score*

```python
     409:                 contribution = weight * layer_scores[layer_key]
     410:                 linear_sum += contribution
>>>  411:                 linear_trace.append({
     412:                     "layer": layer_key,
     413:                     "weight": weight,
```

#### Line 423 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: layer1, layer2)" format
            pair_str = pair_key.strip("()")
            *

```python
     421: 
     422:         for pair_key, weight in interaction_weights.items():
>>>  423:             # Parse "(layer1, layer2)" format
     424:             pair_str = pair_key.strip("()")
     425:             layer1, layer2 = [l.strip() for l in pair_str.split(",")]
```

#### Line 431 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight, layer1_score, layer2_score*

```python
     429:                 contribution = weight * min_score
     430:                 interaction_sum += contribution
>>>  431:                 interaction_trace.append({
     432:                     "pair": pair_key,
     433:                     "weight": weight,
```

#### Line 449 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: total_weight:.6*

```python
     447:             raise CalibrationConfigError(
     448:                 f"Fusion weights misconfigured for role {role.value}: "
>>>  449:                 f"total_weight={total_weight:.6f} produced calibrated_score={calibrated_score:.6f}. "
     450:                 f"Score must be in [0,1]. Weight constraints violated. "
     451:                 f"Check fusion_specification.json and ensure Σ(a_ℓ) + Σ(a_ℓk) ≤ 1."
```

#### Line 449 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: calibrated_score:.6*

```python
     447:             raise CalibrationConfigError(
     448:                 f"Fusion weights misconfigured for role {role.value}: "
>>>  449:                 f"total_weight={total_weight:.6f} produced calibrated_score={calibrated_score:.6f}. "
     450:                 f"Score must be in [0,1]. Weight constraints violated. "
     451:                 f"Check fusion_specification.json and ensure Σ(a_ℓ) + Σ(a_ℓk) ≤ 1."
```

#### Line 534 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: fusion_weights, intrinsic_calibration*

```python
     532:         )
     533: 
>>>  534:         parameter_provenance = {
     535:             "fusion_weights": {
     536:                 "source": "fusion_specification.json",
```

#### Line 535 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: linear_weights, interaction_weights*

```python
     533: 
     534:         parameter_provenance = {
>>>  535:             "fusion_weights": {
     536:                 "source": "fusion_specification.json",
     537:                 "role": role.value,
```

#### Line 548 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: runtime_metrics, layer_computations*

```python
     546: 
     547:         # Build evidence trail
>>>  548:         evidence_trail = {
     549:             "pdt_metrics": evidence_store.pdt_structure,
     550:             "runtime_metrics": evidence_store.runtime_metrics,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/intrinsic_calibration_loader.py

**5 violation(s)**

#### Line 6 - `HARDCODED_LAYER_SCORE` [MEDIUM]

*Pattern matched: @b = 0.5*

```python
       4: This module provides the ONLY interface for loading intrinsic calibration data.
       5: Enforces strict @b-only access with fallback behavior:
>>>    6: - pending → @b = 0.5 (neutral baseline)
       7: - excluded → @b = None (causes method skip)
       8: - none → @b = 0.3 (low confidence with warning)
```

#### Line 8 - `HARDCODED_LAYER_SCORE` [MEDIUM]

*Pattern matched: @b = 0.3*

```python
       6: - pending → @b = 0.5 (neutral baseline)
       7: - excluded → @b = None (causes method skip)
>>>    8: - none → @b = 0.3 (low confidence with warning)
       9: - computed → actual @b values from JSON
      10: 
```

#### Line 95 - `HARDCODED_LAYER_SCORE` [MEDIUM]

*Pattern matched: @b=0.3*

```python
      93:             logger.warning(
      94:                 f"Method '{method_id}' not in calibration registry. "
>>>   95:                 f"Applying fallback: status='none', @b=0.3"
      96:             )
      97:             return IntrinsicCalibration(
```

#### Line 128 - `HARDCODED_LAYER_SCORE` [MEDIUM]

*Pattern matched: @b=0.5*

```python
     126: 
     127:         if status == "pending":
>>>  128:             logger.info(f"Method '{method_id}' is pending, applying fallback @b=0.5")
     129:             return IntrinsicCalibration(
     130:                 method_id=method_id,
```

#### Line 142 - `HARDCODED_LAYER_SCORE` [MEDIUM]

*Pattern matched: @b=0.3*

```python
     140:         if status == "none":
     141:             logger.warning(
>>>  142:                 f"Method '{method_id}' has status='none', applying fallback @b=0.3"
     143:             )
     144:             return IntrinsicCalibration(
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/layer_assignment.py

**9 violation(s)**

#### Line 2 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: Layer Assignment System for Calibration

This module defines the canonical layer*

```python
       1: """
>>>    2: Layer Assignment System for Calibration
       3: 
       4: This module defines the canonical layer requirements for all method roles
```

#### Line 5 - `HARDCODED_CHOQUET_WEIGHTS` [MEDIUM]

*Pattern matched: Choquet integral weights for executors.

Layers:
- @b: Code quality (base theory*

```python
       3: 
       4: This module defines the canonical layer requirements for all method roles
>>>    5: and provides layer assignment with Choquet integral weights for executors.
       6: 
       7: Layers:
```

#### Line 21 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      19: from typing import Any
      20: 
>>>   21: LAYER_REQUIREMENTS: dict[str, list[str]] = {
      22:     "ingest": ["@b", "@chain", "@u", "@m"],
      23:     "processor": ["@b", "@chain", "@u", "@m"],
```

#### Line 115 - `HARDCODED_CHOQUET_WEIGHTS` [MEDIUM]

*Pattern matched: CHOQUET_WEIGHTS[layer] for layer in layers}

    interaction_weights = {*

```python
     113:     layers = LAYER_REQUIREMENTS[role]
     114: 
>>>  115:     weights = {layer: CHOQUET_WEIGHTS[layer] for layer in layers}
     116: 
     117:     interaction_weights = {}
```

#### Line 117 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'interaction_weights' assigned inline dict literal*

```python
     115:     weights = {layer: CHOQUET_WEIGHTS[layer] for layer in layers}
     116: 
>>>  117:     interaction_weights = {}
     118:     for (l1, l2), weight in CHOQUET_INTERACTION_WEIGHTS.items():
     119:         if l1 in layers and l2 in layers:
```

#### Line 118 - `HARDCODED_CHOQUET_WEIGHTS` [MEDIUM]

*Pattern matched: CHOQUET_INTERACTION_WEIGHTS.items():
        if l1 in layers and l2 in layers:
 *

```python
     116: 
     117:     interaction_weights = {}
>>>  118:     for (l1, l2), weight in CHOQUET_INTERACTION_WEIGHTS.items():
     119:         if l1 in layers and l2 in layers:
     120:             interaction_weights[f"{l1},{l2}"] = weight
```

#### Line 131 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layers, weights, interaction_weights*

```python
     129:         interaction_weights = {k: v * scale for k, v in interaction_weights.items()}
     130: 
>>>  131:     return {
     132:         "method_id": method_id,
     133:         "role": role,
```

#### Line 159 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layer_system*

```python
     157: 
     158:     inventory = {
>>>  159:         "_metadata": {
     160:             "version": "1.0.0",
     161:             "description": "Canonical layer assignments for F.A.R.F.A.N. calibration system",
```

#### Line 200 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layers, weights, interaction_weights*

```python
     198:             )
     199: 
>>>  200:         inventory["methods"][executor["method_id"]] = {
     201:             "method_id": assignment["method_id"],
     202:             "role": assignment["role"],
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/layer_coexistence.py

**10 violation(s)**

#### Line 97 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: active_layers, calibration_rule*

```python
      95:     def to_dict(self) -> Dict:
      96:         """Export to dictionary for serialization"""
>>>   97:         return {
      98:             'method_id': self.method_id,
      99:             'active_layers': [layer.value for layer in self.active_layers],
```

#### Line 240 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight:.4*

```python
     238: 
     239:         for i, score in enumerate(scores):
>>>  240:             trace.append(f"  Layer {score.layer.value}: x = {score.value:.4f}, w = {score.weight:.4f}")
     241: 
     242:         weighted_sum = sum(s.value * s.weight for s in scores)
```

#### Line 245 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weighted_sum:.4*

```python
     243:         weight_sum = sum(s.weight for s in scores)
     244: 
>>>  245:         trace.append(f"Weighted sum: Σ(w·x) = {weighted_sum:.4f}")
     246:         trace.append(f"Weight sum: Σ(w) = {weight_sum:.4f}")
     247:         if weight_sum == 0:
```

#### Line 246 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight_sum:.4*

```python
     244: 
     245:         trace.append(f"Weighted sum: Σ(w·x) = {weighted_sum:.4f}")
>>>  246:         trace.append(f"Weight sum: Σ(w) = {weight_sum:.4f}")
     247:         if weight_sum == 0:
     248:             trace.append(f"Result: No valid weights, returning 0.0")
```

#### Line 250 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weighted_sum:.4*

```python
     248:             trace.append(f"Result: No valid weights, returning 0.0")
     249:         else:
>>>  250:             trace.append(f"Result: {weighted_sum:.4f} / {weight_sum:.4f} = {weighted_sum/weight_sum:.4f}")
     251: 
     252:         return trace
```

#### Line 250 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight_sum:.4*

```python
     248:             trace.append(f"Result: No valid weights, returning 0.0")
     249:         else:
>>>  250:             trace.append(f"Result: {weighted_sum:.4f} / {weight_sum:.4f} = {weighted_sum/weight_sum:.4f}")
     251: 
     252:         return trace
```

#### Line 250 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight_sum:.4*

```python
     248:             trace.append(f"Result: No valid weights, returning 0.0")
     249:         else:
>>>  250:             trace.append(f"Result: {weighted_sum:.4f} / {weight_sum:.4f} = {weighted_sum/weight_sum:.4f}")
     251: 
     252:         return trace
```

#### Line 320 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weights_sum_to_one*

```python
     318:         weight_sum = sum(self.position_weights)
     319: 
>>>  320:         return {
     321:             'monotonic': True,  # Always true if weights are non-negative
     322:             'bounded': 0 <= result <= 1,
```

#### Line 342 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight:.4*

```python
     340:             weight_idx = min(i, len(self.position_weights) - 1)
     341:             weight = self.position_weights[weight_idx]
>>>  342:             trace.append(f"  Position {i+1}: {layer} = {val:.4f}, weight = {weight:.4f}")
     343: 
     344:         result = self.fuse(scores)
```

#### Line 351 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: WeightedAverage*

```python
     349: 
     350: # Registry of available fusion operators
>>>  351: FUSION_OPERATORS = {
     352:     'WeightedAverage': WeightedAverageFusion,
     353:     'OWA': OWAFusion,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/layer_influence_model.py

**2 violation(s)**

#### Line 2 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: Layer Coexistence and Influence Model - Formal Specification

This module encode*

```python
       1: """
>>>    2: Layer Coexistence and Influence Model - Formal Specification
       3: 
       4: This module encodes the mathematical relationships between layers,
```

#### Line 160 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
     158:             strength=1.0,
     159:             functional_form="active(@p) ⟺ |scored_dimensions| ≥ 3",
>>>  160:             conditions={'threshold': 3}
     161:         ))
     162: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/meta_layer.py

**7 violation(s)**

#### Line 2 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: Layer (@m) - Full Implementation.

Evaluates governance compliance using weighte*

```python
       1: """
>>>    2: Meta Layer (@m) - Full Implementation.
       3: 
       4: Evaluates governance compliance using weighted formula:
```

#### Line 5 - `HARDCODED_LAYER_SCORE` [MEDIUM]

*Pattern matched: @m = 0.5*

```python
       3: 
       4: Evaluates governance compliance using weighted formula:
>>>    5: x_@m = 0.5·m_transp + 0.4·m_gov + 0.1·m_cost
       6: """
       7: import logging
```

#### Line 79 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      77:             formula_exported, full_trace, logs_conform
      78:         )
>>>   79:         logger.debug("m_transp_computed", extra={"score": m_transp})
      80: 
      81:         # Component 2: Governance (m_gov)
```

#### Line 85 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      83:             method_version, config_hash, signature_valid
      84:         )
>>>   85:         logger.debug("m_gov_computed", extra={"score": m_gov})
      86: 
      87:         # Component 3: Cost (m_cost)
```

#### Line 89 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
      87:         # Component 3: Cost (m_cost)
      88:         m_cost = self._compute_cost(execution_time_s)
>>>   89:         logger.debug("m_cost_computed", extra={"score": m_cost})
      90: 
      91:         # Weighted sum
```

#### Line 178 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: runtime.

        Scoring:
            1.0: < threshold_fast (e.g., <1s)
       *

```python
     176:     def _compute_cost(self, execution_time_s: Optional[float] = None) -> float:
     177:         """
>>>  178:         Compute m_cost based on runtime.
     179: 
     180:         Scoring:
```

#### Line 204 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: runtime, threshold*

```python
     202:             logger.warning(
     203:                 "meta_slow_execution",
>>>  204:                 extra={
     205:                     "runtime": execution_time_s,
     206:                     "threshold": self.config.threshold_acceptable
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/rigorous_calibration_triage.py

**12 violation(s)**

#### Line 3 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: Intrinsic Calibration Triage - Method by Method Analysis

Per tesislizayjuan-deb*

```python
       1: #!/usr/bin/env python3
       2: """
>>>    3: Rigorous Intrinsic Calibration Triage - Method by Method Analysis
       4: 
       5: Per tesislizayjuan-debug requirements (comments 3512949686, 3513311176):
```

#### Line 110 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layer_is_critical*

```python
     108:             "matched_verbs_in_doc": q1_matches_doc
     109:         },
>>>  110:         "q2_parametric": {
     111:             "result": q2_parametric,
     112:             "matched_keywords": q2_matches,
```

#### Line 115 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layer_is_critical*

```python
     113:             "layer_is_critical": layer in critical_layers
     114:         },
>>>  115:         "q3_safety_critical": {
     116:             "result": q3_safety_critical,
     117:             "layer_is_critical": layer in safety_layers,
```

#### Line 201 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: final_score*

```python
     199: 
     200:     # Machine-readable evidence
>>>  201:     evidence = {
     202:         "formula": "b_theory = 0.4*stat + 0.3*logic + 0.3*assumptions",
     203:         "components": {
```

#### Line 292 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: final_score*

```python
     290: 
     291:     # Machine-readable evidence
>>>  292:     evidence = {
     293:         "formula": "b_impl = 0.35*test + 0.25*type + 0.25*error + 0.15*doc",
     294:         "components": {
```

#### Line 338 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: layer = method_info.get('layer', 'unknown')
    
    # Load rubric rules
    b_d*

```python
     336:     Uses machine-readable rules from rubric config
     337:     """
>>>  338:     layer = method_info.get('layer', 'unknown')
     339: 
     340:     # Load rubric rules
```

#### Line 367 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: final_score*

```python
     365: 
     366:     # Machine-readable evidence
>>>  367:     evidence = {
     368:         "formula": "b_deploy = 0.4*validation + 0.35*stability + 0.25*failure",
     369:         "components": {
```

#### Line 369 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: layer_maturity_baseline, stability_coefficient*

```python
     367:     evidence = {
     368:         "formula": "b_deploy = 0.4*validation + 0.35*stability + 0.25*failure",
>>>  369:         "components": {
     370:             "layer_maturity_baseline": {
     371:                 "layer": layer,
```

#### Line 384 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: layer_maturity_baseline * 0.9",
                "computation": f"{base_maturity}*

```python
     382:                 "weight": weights['stability_coefficient'],
     383:                 "score": round(stability_score, 3),
>>>  384:                 "formula": "layer_maturity_baseline * 0.9",
     385:                 "computation": f"{base_maturity} * 0.9 = {round(stability_score, 3)}"
     386:             },
```

#### Line 414 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: calibration_status, layer*

```python
     412:     if not requires_cal:
     413:         # Excluded method
>>>  414:         return {
     415:             "method_id": canonical_name,
     416:             "calibration_status": "excluded",
```

#### Line 431 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: b_theory, b_impl, b_deploy*

```python
     429: 
     430:     # Pass 3: Create calibration profile with machine-readable evidence
>>>  431:     return {
     432:         "method_id": canonical_name,
     433:         "b_theory": b_theory,
```

#### Line 436 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: b_theory_computation, b_impl_computation, b_deploy_computation*

```python
     434:         "b_impl": b_impl,
     435:         "b_deploy": b_deploy,
>>>  436:         "evidence": {
     437:             "triage_decision": triage_evidence,
     438:             "triage_reason": reason,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/unit_layer.py

**20 violation(s)**

#### Line 2 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: Layer (@u) - PRODUCTION IMPLEMENTATION.

Evaluates PDT quality through 4 compone*

```python
       1: """
>>>    2: Unit Layer (@u) - PRODUCTION IMPLEMENTATION.
       3: 
       4: Evaluates PDT quality through 4 components: S, M, I, P.
```

#### Line 43 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score=0.0*

```python
      41:             return LayerScore(
      42:                 layer=LayerID.UNIT,
>>>   43:                 score=0.0,
      44:                 components={"S": S, "gate_failure": "structural"},
      45:                 rationale=f"HARD GATE: S={S:.2f} < {self.config.min_structural_compliance}",
```

#### Line 46 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
      44:                 components={"S": S, "gate_failure": "structural"},
      45:                 rationale=f"HARD GATE: S={S:.2f} < {self.config.min_structural_compliance}",
>>>   46:                 metadata={"gate": "structural", "threshold": self.config.min_structural_compliance}
      47:             )
      48: 
```

#### Line 60 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: LayerScore(
                layer=LayerID.UNIT,
                score=0.0,
     *

```python
      58:         # Step 5: Check hard gate for I_struct
      59:         if I_components["I_struct"] < self.config.i_struct_hard_gate:
>>>   60:             return LayerScore(
      61:                 layer=LayerID.UNIT,
      62:                 score=0.0,
```

#### Line 62 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score=0.0*

```python
      60:             return LayerScore(
      61:                 layer=LayerID.UNIT,
>>>   62:                 score=0.0,
      63:                 components={"S": S, "M": M, "I_struct": I_components["I_struct"]},
      64:                 rationale=f"HARD GATE: I_struct={I_components['I_struct']:.2f} < {self.config.i_struct_hard_gate}",
```

#### Line 77 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score=0.0*

```python
      75:             return LayerScore(
      76:                 layer=LayerID.UNIT,
>>>   77:                 score=0.0,
      78:                 components={"S": S, "M": M, "I": I, "gate_failure": "ppi_presence"},
      79:                 rationale="HARD GATE: PPI required but not present",
```

#### Line 86 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score=0.0*

```python
      84:             return LayerScore(
      85:                 layer=LayerID.UNIT,
>>>   86:                 score=0.0,
      87:                 components={"S": S, "M": M, "I": I, "P": P, "gate_failure": "indicator_matrix"},
      88:                 rationale="HARD GATE: Indicator matrix required but not present",
```

#### Line 174 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight*

```python
     172:         # Section requirements (from config)
     173:         requirements = {
>>>  174:             "Diagnóstico": {
     175:                 "min_tokens": self.config.diagnostico_min_tokens,
     176:                 "min_keywords": self.config.diagnostico_min_keywords,
```

#### Line 181 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight*

```python
     179:                 "weight": self.config.critical_sections_weight,  # Critical section
     180:             },
>>>  181:             "Parte Estratégica": {
     182:                 "min_tokens": self.config.estrategica_min_tokens,
     183:                 "min_keywords": self.config.estrategica_min_keywords,
```

#### Line 187 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight*

```python
     185:                 "weight": self.config.critical_sections_weight,  # Critical section
     186:             },
>>>  187:             "PPI": {
     188:                 "min_tokens": self.config.ppi_section_min_tokens,
     189:                 "min_keywords": self.config.ppi_section_min_keywords,
```

#### Line 193 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight*

```python
     191:                 "weight": self.config.critical_sections_weight,  # Critical section
     192:             },
>>>  193:             "Seguimiento": {
     194:                 "min_tokens": self.config.seguimiento_min_tokens,
     195:                 "min_keywords": self.config.seguimiento_min_keywords,
```

#### Line 199 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight*

```python
     197:                 "weight": 1.0,
     198:             },
>>>  199:             "Marco Normativo": {
     200:                 "min_tokens": self.config.marco_normativo_min_tokens,
     201:                 "min_keywords": self.config.marco_normativo_min_keywords,
```

#### Line 206 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'total_weight' assigned hardcoded value: 0.0*

```python
     204:         }
     205: 
>>>  206:         total_weight = 0.0
     207:         weighted_score = 0.0
     208: 
```

#### Line 206 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: total_weight = 0.0*

```python
     204:         }
     205: 
>>>  206:         total_weight = 0.0
     207:         weighted_score = 0.0
     208: 
```

#### Line 207 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'weighted_score' assigned hardcoded value: 0.0*

```python
     205: 
     206:         total_weight = 0.0
>>>  207:         weighted_score = 0.0
     208: 
     209:         for section_name, reqs in requirements.items():
```

#### Line 207 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weighted_score = 0.0*

```python
     205: 
     206:         total_weight = 0.0
>>>  207:         weighted_score = 0.0
     208: 
     209:         for section_name, reqs in requirements.items():
```

#### Line 214 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'score' assigned hardcoded value: 0.0*

```python
     212:             if not section_data.get("present", False):
     213:                 # Missing section gets 0
>>>  214:                 score = 0.0
     215:             else:
     216:                 # Check all requirements
```

#### Line 214 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score = 0.0*

```python
     212:             if not section_data.get("present", False):
     213:                 # Missing section gets 0
>>>  214:                 score = 0.0
     215:             else:
     216:                 # Check all requirements
```

#### Line 265 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'total_struct_score' assigned hardcoded value: 0.0*

```python
     263:         optional_fields = ["Año LB", "Código MGA"]
     264: 
>>>  265:         total_struct_score = 0.0
     266:         for row in pdt.indicator_rows:
     267:             critical_present = sum(1 for f in critical_fields if row.get(f))
```

#### Line 265 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: total_struct_score = 0.0*

```python
     263:         optional_fields = ["Año LB", "Código MGA"]
     264: 
>>>  265:         total_struct_score = 0.0
     266:         for row in pdt.indicator_rows:
     267:             critical_present = sum(1 for f in critical_fields if row.get(f))
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/calibration/validators.py

**1 violation(s)**

#### Line 225 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'intrinsic' assigned inline dict literal*

```python
     223:         except Exception as e:
     224:             all_errors.append(f"Failed to load intrinsic_calibration.json: {e}")
>>>  225:             intrinsic = {}
     226: 
     227:         # Validate contextual config exists (full validation TBD)
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/method_inventory.py

**4 violation(s)**

#### Line 203 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'has_hardcoded_calibration' assigned hardcoded value: False*

```python
     201: def compute_governance_flags_for_file(module_ast: ast.Module) -> GovernanceFlags:
     202:     uses_yaml = False
>>>  203:     has_hardcoded_calibration = False
     204:     has_hardcoded_timeout = False
     205:     suspicious_magic_numbers: list[str] = []
```

#### Line 215 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yml"*

```python
     213: 
     214:         if isinstance(node, ast.Constant) and isinstance(node.value, str):
>>>  215:             if node.value.endswith((".yml", ".yaml")):
     216:                 uses_yaml = True
     217: 
```

#### Line 215 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yaml"*

```python
     213: 
     214:         if isinstance(node, ast.Constant) and isinstance(node.value, str):
>>>  215:             if node.value.endswith((".yml", ".yaml")):
     216:                 uses_yaml = True
     217: 
```

#### Line 235 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'has_hardcoded_calibration' assigned hardcoded value: True*

```python
     233:                     cal_tokens = ["b_theory", "b_impl", "b_deploy", "quality_threshold", "evidence_snippets", "priority_score"]
     234:                     if any(t in target_name for t in cal_tokens):
>>>  235:                          has_hardcoded_calibration = True
     236:                          suspicious_magic_numbers.append(f"{target_name} assigned literal")
     237: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/observability/metrics.py

**1 violation(s)**

#### Line 363 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: calibration_mode_total, current_runtime_mode*

```python
     361:         Dictionary of all metric collectors
     362:     """
>>>  363:     return {
     364:         'fallback_activations_total': fallback_activations_total,
     365:         'segmentation_method_total': segmentation_method_total,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/arg_router.py

**1 violation(s)**

#### Line 523 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: _calculate_confidence_score, _analyze_coherence_score, _validate_threshold_compliance*

```python
     521:             Dict mapping method names to route specs
     522:         """
>>>  523:         routes = {
     524:             "_extract_quantitative_claims": {
     525:                 "required_args": ["content"],
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/base_executor_with_contract.py

**2 violation(s)**

#### Line 17 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: runtime avoids import to break cycles
    MethodExecutor = Any
    PreprocessedD*

```python
      15:     from farfan_pipeline.core.orchestrator.core import MethodExecutor
      16:     from farfan_pipeline.core.types import PreprocessedDocument
>>>   17: else:  # pragma: no cover - runtime avoids import to break cycles
      18:     MethodExecutor = Any
      19:     PreprocessedDocument = Any
```

#### Line 637 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
     635:                     if signal_pack is not None:
     636:                         signal_usage_list.append(
>>>  637:                             {
     638:                                 "method": f"{class_name}.{method_name}",
     639:                                 "policy_area": signal_pack.policy_area,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/class_registry.py

**1 violation(s)**

#### Line 14 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: BayesianEvidenceScorer*

```python
      12: 
      13: # Map of orchestrator-facing class names to their import paths.
>>>   14: _CLASS_PATHS: Mapping[str, str] = {
      15:     "IndustrialPolicyProcessor": "farfan_core.processing.policy_processor.IndustrialPolicyProcessor",
      16:     "PolicyTextProcessor": "farfan_core.processing.policy_processor.PolicyTextProcessor",
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/core.py

**14 violation(s)**

#### Line 103 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: RuntimeError):
    """Raised when a phase exceeds its timeout."""

    def __ini*

```python
     101: 
     102: 
>>>  103: class PhaseTimeoutError(RuntimeError):
     104:     """Raised when a phase exceeds its timeout."""
     105: 
```

#### Line 1831 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
    1829:         if self.abort_signal.is_aborted():
    1830:             score = min(score, 20.0)
>>> 1831:         return {
    1832:             "score": score,
    1833:             "resource_usage": usage,
```

#### Line 1858 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: calibrations_loaded*

```python
    1856:         # Check method executor
    1857:         try:
>>> 1858:             executor_health = {
    1859:                 "instances_loaded": len(self.executor.instances),
    1860:                 "calibrations_loaded": len(self.executor.calibrations),
```

#### Line 2008 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: RuntimeError(
                    "Method map is empty - cannot route methods. "*

```python
    2006:             # ========================================================================
    2007:             if not method_map:
>>> 2008:                 raise RuntimeError(
    2009:                     "Method map is empty - cannot route methods. "
    2010:                     "A non-empty method map is required for orchestration."
```

#### Line 2750 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
    2748:             )
    2749:             scored_payloads.append(
>>> 2750:                 {
    2751:                     "question_global": item.question_global,
    2752:                     "base_slot": item.base_slot,
```

#### Line 2974 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score=0.0*

```python
    2972:             logger.error("No monolith in config for macro evaluation")
    2973:             macro_score = MacroScore(
>>> 2974:                 score=0.0,
    2975:                 quality_level="INSUFICIENTE",
    2976:                 cross_cutting_coherence=0.0,
```

#### Line 2983 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: macro_score, macro_score_normalized, cluster_scores*

```python
    2981:                 validation_details={"error": "No monolith", "type": "config"},
    2982:             )
>>> 2983:             result: MacroScoreDict = {
    2984:                 "macro_score": macro_score,
    2985:                 "macro_score_normalized": 0.0,
```

#### Line 3041 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score=0.0*

```python
    3039:             logger.error(f"Failed to evaluate macro: {e}")
    3040:             macro_score = MacroScore(
>>> 3041:                 score=0.0,
    3042:                 quality_level="INSUFICIENTE",
    3043:                 cross_cutting_coherence=0.0,
```

#### Line 3060 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: macro_score, macro_score_normalized, cluster_scores*

```python
    3058:         )
    3059: 
>>> 3060:         result: MacroScoreDict = {
    3061:             "macro_score": macro_score,
    3062:             "macro_score_normalized": macro_score_normalized,
```

#### Line 3102 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: macro_score*

```python
    3100:                 "RecommendationEngine not available, returning empty recommendations"
    3101:             )
>>> 3102:             recommendations = {
    3103:                 "MICRO": {
    3104:                     "level": "MICRO",
```

#### Line 3190 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
    3188:                     weak_pa = weakest_area[0].get("area_id") if weakest_area else None
    3189: 
>>> 3190:                     cluster_data[cluster_id] = {
    3191:                         "score": normalized_cluster_score
    3192:                         * self.PERCENTAGE_SCALE,  # 0-100 scale
```

#### Line 3284 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority_micro_gaps, macro_score_percentage*

```python
    3282:             priority_micro_gaps = [k for k, v in sorted_micro[:5] if v < 0.55]
    3283: 
>>> 3284:             macro_data = {
    3285:                 "macro_band": macro_band,
    3286:                 "clusters_below_target": clusters_below_target,
```

#### Line 3303 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: macro_score*

```python
    3301:             # GENERATE RECOMMENDATIONS AT ALL 3 LEVELS
    3302:             # ========================================================================
>>> 3303:             context = {
    3304:                 "generated_at": datetime.utcnow().isoformat(),
    3305:                 "macro_score": macro_score,
```

#### Line 3334 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: macro_score*

```python
    3332:         except Exception as e:
    3333:             logger.error(f"Error generating recommendations: {e}", exc_info=True)
>>> 3334:             recommendations = {
    3335:                 "MICRO": {
    3336:                     "level": "MICRO",
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/executors.py

**33 violation(s)**

#### Line 190 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: RuntimeError("A valid MethodExecutor instance is required for executor injection*

```python
     188:         self.config = config
     189:         if not isinstance(method_executor, MethodExecutor):
>>>  190:             raise RuntimeError("A valid MethodExecutor instance is required for executor injection.")
     191:         self.method_executor = method_executor
     192:         self.execution_log = []
```

#### Line 643 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: confidence_scores*

```python
     641:         )
     642: 
>>>  643:         raw_evidence = {
     644:             "magnitude_indicators": {
     645:                 "allocation_gaps": allocation_gaps,
```

#### Line 759 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: financial_score, risk_priorities*

```python
     757:         )
     758: 
>>>  759:         raw_evidence = {
     760:             "budget_allocations": allocation_trace,
     761:             "program_mappings": program_matches,
```

#### Line 861 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: specificity_scores*

```python
     859:         )
     860: 
>>>  861:         raw_evidence = {
     862:             "entities_identified": consolidated,
     863:             "entity_types": entity_types,
```

#### Line 1237 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: composite_likelihood, prior_initialization, type_transition_prior*

```python
    1235:         )
    1236: 
>>> 1237:         raw_evidence = {
    1238:             "root_causes_identified": [link.get("root_cause") for link in (causal_links or [])],
    1239:             "activity_linkages": causal_links,
```

#### Line 1339 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: risk_priorities*

```python
    1337:         )
    1338: 
>>> 1339:         raw_evidence = {
    1340:             "operational_risks": [r for r in risk_inference if r.get("type") == "operational"],
    1341:             "social_risks": [r for r in risk_inference if r.get("type") == "social"],
```

#### Line 1426 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_scores, adaptive_likelihood*

```python
    1424:         )
    1425: 
>>> 1426:         raw_evidence = {
    1427:             "complementarity_evidence": coherence_metrics.get("complementarity", []),
    1428:             "sequential_logic": sequence_audit,
```

#### Line 1430 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: objective_alignment*

```python
    1428:             "sequential_logic": sequence_audit,
    1429:             "logical_incompatibilities": incompatibilities,
>>> 1430:             "coherence_scores": {
    1431:                 "overall_coherence": coherence_metrics,
    1432:                 "objective_alignment": objective_alignment,
```

#### Line 1445 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_score*

```python
    1443:             "executor_id": self.executor_id,
    1444:             "raw_evidence": raw_evidence,
>>> 1445:             "metadata": {
    1446:                 "methods_executed": [log["method"] for log in self.execution_log],
    1447:                 "incompatibilities_found": len(incompatibilities),
```

#### Line 1522 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: indicator_quality_scores, overall_quality_score*

```python
    1520:         )
    1521: 
>>> 1522:         raw_evidence = {
    1523:             "indicators_with_baseline": [i for i in indicator_scores if i.get("has_baseline")],
    1524:             "indicators_with_target": [i for i in indicator_scores if i.get("has_target")],
```

#### Line 1633 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_score*

```python
    1631:         proportionality_recommendations = self._execute_method(
    1632:             "PDETMunicipalPlanAnalyzer", "_generate_recommendations", context,
>>> 1633:             analysis_results={
    1634:                 "financial_analysis": financial_feasibility,
    1635:                 "quality_score": quality_score
```

#### Line 1665 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'domain_scores' assigned inline dict literal*

```python
    1663:             "AdaptivePriorCalculator", "calculate_likelihood_adaptativo", context
    1664:         )
>>> 1665:         domain_scores = {
    1666:             "structural": sufficiency_calc.get("coverage_ratio", 0.0),
    1667:             "financial": financial_feasibility.get("sustainability_score", 0.0),
```

#### Line 1699 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: proportionality_score, financial_component_score, adjusted_domain_weights*

```python
    1697:         )
    1698: 
>>> 1699:         raw_evidence = {
    1700:             "target_population_size": context.get("diagnosed_universe", 0),
    1701:             "product_targets": context.get("product_targets", []),
```

#### Line 1900 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: responsibility_clarity_score, policy_domain_scores*

```python
    1898:         )
    1899: 
>>> 1900:         raw_evidence = {
    1901:             "budgetary_traceability": {
    1902:                 "bpin_codes": [m.get("bpin") for m in (program_matches or []) if m.get("bpin")],
```

#### Line 2021 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight=1.0*

```python
    2019:             source="temp_node",
    2020:             target="temp_target",
>>> 2021:             weight=1.0
    2022:         )
    2023:         node_export = self._execute_method(
```

#### Line 2070 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: threshold=10.0*

```python
    2068:             value=graph_stats.get("edges", 0),
    2069:             unit="edges",
>>> 2070:             threshold=10.0
    2071:         )
    2072:         engine_readiness = self._execute_method(
```

#### Line 2106 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: feasibility_score*

```python
    2104:         )
    2105: 
>>> 2106:         raw_evidence = {
    2107:             "activity_product_mapping": connection_validation,
    2108:             "resource_adequacy": (performance_analysis or {}).get("resource_fit", {}),
```

#### Line 2110 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: necessity_score*

```python
    2108:             "resource_adequacy": (performance_analysis or {}).get("resource_fit", {}),
    2109:             "timeline_feasibility": (performance_analysis or {}).get("timeline_feasibility", {}),
>>> 2110:             "technical_validation": {
    2111:                 "dag_valid": is_acyclic,
    2112:                 "acyclicity_p": acyclicity_pvalue,
```

#### Line 2125 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: resource_likelihood*

```python
    2123:                 "statistical_power": stat_power
    2124:             },
>>> 2125:             "performance_metrics": {
    2126:                 "benchmarks": performance_benchmarks,
    2127:                 "loss_functions": loss_functions,
```

#### Line 2142 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: feasibility_score*

```python
    2140:             "executor_id": self.executor_id,
    2141:             "raw_evidence": raw_evidence,
>>> 2142:             "metadata": {
    2143:                 "methods_executed": [log["method"] for log in self.execution_log],
    2144:                 "dag_is_valid": is_acyclic,
```

#### Line 2256 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_score*

```python
    2254:         causal_recommendations = self._execute_method(
    2255:             "PDETMunicipalPlanAnalyzer", "_generate_recommendations", context,
>>> 2256:             analysis_results={"financial_analysis": financial_analysis, "quality_score": getattr(causal_dag, 'graph', {})}
    2257:         )
    2258:         factual_eval = None
```

#### Line 2554 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: temporal_consistency_score, composite_likelihood*

```python
    2552:         )
    2553: 
>>> 2554:         raw_evidence = {
    2555:             "outcome_indicators": outcome_mentions,
    2556:             "indicators_with_baseline": [o for o in outcome_mentions if o.get("has_baseline")],
```

#### Line 2833 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: prioritized_problems, solvency_score, risk_priorities*

```python
    2831:         )
    2832: 
>>> 2833:         raw_evidence = {
    2834:             "prioritized_problems": context.get("diagnosis_problems", []),
    2835:             "proposed_results": context.get("outcome_indicators", []),
```

#### Line 2906 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: pnd_alignment, sdg_alignment, pdet_alignment*

```python
    2904:         )
    2905: 
>>> 2906:         raw_evidence = {
    2907:             "pnd_alignment": dnp_compliance,
    2908:             "sdg_alignment": context.get("sdg_mappings", []),
```

#### Line 3151 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: omission_score=1*

```python
    3149:         risk_prioritization = self._execute_method(
    3150:             "BayesianCounterfactualAuditor", "aggregate_risk_and_prioritize", context,
>>> 3151:             omission_score=1 - quality_score.financial_feasibility if hasattr(quality_score, "financial_feasibility") else 0.2,
    3152:             insufficiency_score=1 - (sufficiency or {}).get("coverage_ratio", 0.0),
    3153:             unnecessity_score=1 - (robustness if isinstance(robustness, (int, float)) else 0.0),
```

#### Line 3152 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: insufficiency_score=1*

```python
    3150:             "BayesianCounterfactualAuditor", "aggregate_risk_and_prioritize", context,
    3151:             omission_score=1 - quality_score.financial_feasibility if hasattr(quality_score, "financial_feasibility") else 0.2,
>>> 3152:             insufficiency_score=1 - (sufficiency or {}).get("coverage_ratio", 0.0),
    3153:             unnecessity_score=1 - (robustness if isinstance(robustness, (int, float)) else 0.0),
    3154:             causal_effect=e_value,
```

#### Line 3153 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: unnecessity_score=1*

```python
    3151:             omission_score=1 - quality_score.financial_feasibility if hasattr(quality_score, "financial_feasibility") else 0.2,
    3152:             insufficiency_score=1 - (sufficiency or {}).get("coverage_ratio", 0.0),
>>> 3153:             unnecessity_score=1 - (robustness if isinstance(robustness, (int, float)) else 0.0),
    3154:             causal_effect=e_value,
    3155:             feasibility=quality_score.financial_feasibility if hasattr(quality_score, "financial_feasibility") else 0.8,
```

#### Line 3200 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_score*

```python
    3198:         exec_report = self._execute_method(
    3199:             "PDETMunicipalPlanAnalyzer", "generate_executive_report", context,
>>> 3200:             analysis_results={"quality_score": quality_dict, "financial_analysis": context.get("financial_analysis", {}) or {"total_budget": 0, "funding_sources": {}, "confidence": (0, 0)}}
    3201:         )
    3202:         export_result = self._execute_method(
```

#### Line 3208 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_scores, risk_prioritization*

```python
    3206:         )
    3207: 
>>> 3208:         raw_evidence = {
    3209:             "composite_indices": context.get("composite_indicators", []),
    3210:             "proxy_indicators": context.get("proxy_indicators", []),
```

#### Line 3247 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: validity_score*

```python
    3245:             "executor_id": self.executor_id,
    3246:             "raw_evidence": raw_evidence,
>>> 3247:             "metadata": {
    3248:                 "methods_executed": [log["method"] for log in self.execution_log],
    3249:                 "composite_indices_count": len(context.get("composite_indicators", [])),
```

#### Line 3510 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: realism_score*

```python
    3508:             "executor_id": self.executor_id,
    3509:             "raw_evidence": raw_evidence,
>>> 3510:             "metadata": {
    3511:                 "methods_executed": [log["method"] for log in self.execution_log],
    3512:                 "realism_score": (predictive_check or {}).get("realism_score", 0),
```

#### Line 3684 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: necessity_score, sufficiency_score*

```python
    3682:         )
    3683: 
>>> 3684:         raw_evidence = {
    3685:             "logical_leaps_detected": (evidential_tests or {}).get("leaps", []),
    3686:             "intervention_scale": context.get("intervention_magnitude", 0),
```

#### Line 3857 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: prior_updates*

```python
    3855:         )
    3856: 
>>> 3857:         raw_evidence = {
    3858:             "monitoring_system_described": len(context.get("monitoring_indicators", [])) > 0,
    3859:             "correction_mechanisms": (feedback_extracted or {}).get("mechanisms", []),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/executors_snapshot/executors.py

**33 violation(s)**

#### Line 174 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: RuntimeError("A valid MethodExecutor instance is required for executor injection*

```python
     172:         self.config = config
     173:         if not isinstance(method_executor, MethodExecutor):
>>>  174:             raise RuntimeError("A valid MethodExecutor instance is required for executor injection.")
     175:         self.method_executor = method_executor
     176:         self.execution_log = []
```

#### Line 464 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: confidence_scores*

```python
     462:         )
     463: 
>>>  464:         raw_evidence = {
     465:             "magnitude_indicators": {
     466:                 "allocation_gaps": allocation_gaps,
```

#### Line 577 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: financial_score, risk_priorities*

```python
     575:         )
     576: 
>>>  577:         raw_evidence = {
     578:             "budget_allocations": allocation_trace,
     579:             "program_mappings": program_matches,
```

#### Line 676 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: specificity_scores*

```python
     674:         )
     675: 
>>>  676:         raw_evidence = {
     677:             "entities_identified": consolidated,
     678:             "entity_types": entity_types,
```

#### Line 1050 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: composite_likelihood*

```python
    1048:         )
    1049: 
>>> 1050:         raw_evidence = {
    1051:             "root_causes_identified": [link.get("root_cause") for link in causal_links],
    1052:             "activity_linkages": causal_links,
```

#### Line 1150 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: risk_priorities*

```python
    1148:         )
    1149: 
>>> 1150:         raw_evidence = {
    1151:             "operational_risks": [r for r in risk_inference if r.get("type") == "operational"],
    1152:             "social_risks": [r for r in risk_inference if r.get("type") == "social"],
```

#### Line 1234 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_scores, adaptive_likelihood*

```python
    1232:         )
    1233: 
>>> 1234:         raw_evidence = {
    1235:             "complementarity_evidence": coherence_metrics.get("complementarity", []),
    1236:             "sequential_logic": sequence_audit,
```

#### Line 1238 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: objective_alignment*

```python
    1236:             "sequential_logic": sequence_audit,
    1237:             "logical_incompatibilities": incompatibilities,
>>> 1238:             "coherence_scores": {
    1239:                 "overall_coherence": coherence_metrics,
    1240:                 "objective_alignment": objective_alignment,
```

#### Line 1253 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_score*

```python
    1251:             "executor_id": self.executor_id,
    1252:             "raw_evidence": raw_evidence,
>>> 1253:             "metadata": {
    1254:                 "methods_executed": [log["method"] for log in self.execution_log],
    1255:                 "incompatibilities_found": len(incompatibilities),
```

#### Line 1330 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: indicator_quality_scores, overall_quality_score*

```python
    1328:         )
    1329: 
>>> 1330:         raw_evidence = {
    1331:             "indicators_with_baseline": [i for i in indicator_scores if i.get("has_baseline")],
    1332:             "indicators_with_target": [i for i in indicator_scores if i.get("has_target")],
```

#### Line 1433 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_score*

```python
    1431:         proportionality_recommendations = self._execute_method(
    1432:             "PDETMunicipalPlanAnalyzer", "_generate_recommendations", context,
>>> 1433:             analysis_results={"financial_analysis": financial_feasibility, "quality_score": quality_score} if 'quality_score' in locals() else {}
    1434:         )
    1435: 
```

#### Line 1462 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'domain_scores' assigned inline dict literal*

```python
    1460:             "AdaptivePriorCalculator", "calculate_likelihood_adaptativo", context
    1461:         )
>>> 1462:         domain_scores = {
    1463:             "structural": sufficiency_calc.get("coverage_ratio", 0.0),
    1464:             "financial": financial_feasibility.get("sustainability_score", 0.0),
```

#### Line 1501 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: proportionality_score, financial_component_score, adjusted_domain_weights*

```python
    1499:         )
    1500: 
>>> 1501:         raw_evidence = {
    1502:             "target_population_size": context.get("diagnosed_universe", 0),
    1503:             "product_targets": context.get("product_targets", []),
```

#### Line 1675 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: responsibility_clarity_score, policy_domain_scores*

```python
    1673:         )
    1674: 
>>> 1675:         raw_evidence = {
    1676:             "budgetary_traceability": {
    1677:                 "bpin_codes": [m.get("bpin") for m in program_matches if m.get("bpin")],
```

#### Line 1783 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight=1.0*

```python
    1781:             source="temp_node",
    1782:             target="temp_target",
>>> 1783:             weight=1.0
    1784:         )
    1785:         node_export = self._execute_method(
```

#### Line 1832 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: threshold=10.0*

```python
    1830:             value=graph_stats.get("edges", 0),
    1831:             unit="edges",
>>> 1832:             threshold=10.0
    1833:         )
    1834:         engine_readiness = self._execute_method(
```

#### Line 1868 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: feasibility_score*

```python
    1866:         )
    1867: 
>>> 1868:         raw_evidence = {
    1869:             "activity_product_mapping": connection_validation,
    1870:             "resource_adequacy": performance_analysis.get("resource_fit", {}),
```

#### Line 1872 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: necessity_score*

```python
    1870:             "resource_adequacy": performance_analysis.get("resource_fit", {}),
    1871:             "timeline_feasibility": performance_analysis.get("timeline_feasibility", {}),
>>> 1872:             "technical_validation": {
    1873:                 "dag_valid": is_acyclic,
    1874:                 "acyclicity_p": acyclicity_pvalue,
```

#### Line 1887 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: resource_likelihood*

```python
    1885:                 "statistical_power": stat_power
    1886:             },
>>> 1887:             "performance_metrics": {
    1888:                 "benchmarks": performance_benchmarks,
    1889:                 "loss_functions": loss_functions,
```

#### Line 1904 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: feasibility_score*

```python
    1902:             "executor_id": self.executor_id,
    1903:             "raw_evidence": raw_evidence,
>>> 1904:             "metadata": {
    1905:                 "methods_executed": [log["method"] for log in self.execution_log],
    1906:                 "dag_is_valid": is_acyclic,
```

#### Line 2009 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_score*

```python
    2007:         causal_recommendations = self._execute_method(
    2008:             "PDETMunicipalPlanAnalyzer", "_generate_recommendations", context,
>>> 2009:             analysis_results={"financial_analysis": financial_analysis, "quality_score": getattr(causal_dag, 'graph', {})}
    2010:         )
    2011:         financial_consistency = None
```

#### Line 2297 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: temporal_consistency_score, composite_likelihood*

```python
    2295:         )
    2296: 
>>> 2297:         raw_evidence = {
    2298:             "outcome_indicators": outcome_mentions,
    2299:             "indicators_with_baseline": [o for o in outcome_mentions if o.get("has_baseline")],
```

#### Line 2573 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: prioritized_problems, solvency_score, risk_priorities*

```python
    2571:         )
    2572: 
>>> 2573:         raw_evidence = {
    2574:             "prioritized_problems": context.get("diagnosis_problems", []),
    2575:             "proposed_results": context.get("outcome_indicators", []),
```

#### Line 2646 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: pnd_alignment, sdg_alignment, pdet_alignment*

```python
    2644:         )
    2645: 
>>> 2646:         raw_evidence = {
    2647:             "pnd_alignment": dnp_compliance,
    2648:             "sdg_alignment": context.get("sdg_mappings", []),
```

#### Line 2885 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: omission_score=1*

```python
    2883:         risk_prioritization = self._execute_method(
    2884:             "BayesianCounterfactualAuditor", "aggregate_risk_and_prioritize", context,
>>> 2885:             omission_score=1 - quality_score.financial_feasibility if hasattr(quality_score, "financial_feasibility") else 0.2,
    2886:             insufficiency_score=1 - sufficiency.get("coverage_ratio", 0.0),
    2887:             unnecessity_score=1 - (robustness if isinstance(robustness, (int, float)) else 0.0),
```

#### Line 2886 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: insufficiency_score=1*

```python
    2884:             "BayesianCounterfactualAuditor", "aggregate_risk_and_prioritize", context,
    2885:             omission_score=1 - quality_score.financial_feasibility if hasattr(quality_score, "financial_feasibility") else 0.2,
>>> 2886:             insufficiency_score=1 - sufficiency.get("coverage_ratio", 0.0),
    2887:             unnecessity_score=1 - (robustness if isinstance(robustness, (int, float)) else 0.0),
    2888:             causal_effect=e_value,
```

#### Line 2887 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: unnecessity_score=1*

```python
    2885:             omission_score=1 - quality_score.financial_feasibility if hasattr(quality_score, "financial_feasibility") else 0.2,
    2886:             insufficiency_score=1 - sufficiency.get("coverage_ratio", 0.0),
>>> 2887:             unnecessity_score=1 - (robustness if isinstance(robustness, (int, float)) else 0.0),
    2888:             causal_effect=e_value,
    2889:             feasibility=quality_score.financial_feasibility if hasattr(quality_score, "financial_feasibility") else 0.8,
```

#### Line 2934 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_score*

```python
    2932:         exec_report = self._execute_method(
    2933:             "PDETMunicipalPlanAnalyzer", "generate_executive_report", context,
>>> 2934:             analysis_results={"quality_score": quality_dict, "financial_analysis": context.get("financial_analysis", {}) or {"total_budget": 0, "funding_sources": {}, "confidence": (0, 0)}}
    2935:         )
    2936:         export_result = self._execute_method(
```

#### Line 2942 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_scores, risk_prioritization*

```python
    2940:         )
    2941: 
>>> 2942:         raw_evidence = {
    2943:             "composite_indices": context.get("composite_indicators", []),
    2944:             "proxy_indicators": context.get("proxy_indicators", []),
```

#### Line 2981 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: validity_score*

```python
    2979:             "executor_id": self.executor_id,
    2980:             "raw_evidence": raw_evidence,
>>> 2981:             "metadata": {
    2982:                 "methods_executed": [log["method"] for log in self.execution_log],
    2983:                 "composite_indices_count": len(context.get("composite_indicators", [])),
```

#### Line 3232 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: realism_score*

```python
    3230:             "executor_id": self.executor_id,
    3231:             "raw_evidence": raw_evidence,
>>> 3232:             "metadata": {
    3233:                 "methods_executed": [log["method"] for log in self.execution_log],
    3234:                 "realism_score": predictive_check.get("realism_score", 0),
```

#### Line 3395 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: necessity_score, sufficiency_score*

```python
    3393:         )
    3394: 
>>> 3395:         raw_evidence = {
    3396:             "logical_leaps_detected": evidential_tests.get("leaps", []),
    3397:             "intervention_scale": context.get("intervention_magnitude", 0),
```

#### Line 3568 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: prior_updates*

```python
    3566:         )
    3567: 
>>> 3568:         raw_evidence = {
    3569:             "monitoring_system_described": len(context.get("monitoring_indicators", [])) > 0,
    3570:             "correction_mechanisms": feedback_extracted.get("mechanisms", []),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/resource_alerts.py

**4 violation(s)**

#### Line 170 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
     168:                 f"({event.memory_mb:.1f} MB)",
     169:                 event=event,
>>>  170:                 metadata={"threshold": self.thresholds.memory_critical_percent},
     171:             )
     172: 
```

#### Line 181 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
     179:                     f"({event.memory_mb:.1f} MB)",
     180:                     event=event,
>>>  181:                     metadata={"threshold": self.thresholds.memory_warning_percent},
     182:                 )
     183: 
```

#### Line 196 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
     194:                 message=f"CPU usage at {event.cpu_percent:.1f}%",
     195:                 event=event,
>>>  196:                 metadata={"threshold": self.thresholds.cpu_critical_percent},
     197:             )
     198: 
```

#### Line 206 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
     204:                     message=f"CPU usage at {event.cpu_percent:.1f}%",
     205:                     event=event,
>>>  206:                     metadata={"threshold": self.thresholds.cpu_warning_percent},
     207:                 )
     208: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/resource_aware_executor.py

**1 violation(s)**

#### Line 73 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
      71:         logger.info(
      72:             f"Executing {executor_id} with resource allocation",
>>>   73:             extra={
      74:                 "max_memory_mb": allocation["max_memory_mb"],
      75:                 "max_workers": allocation["max_workers"],
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/resource_manager.py

**2 violation(s)**

#### Line 518 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: priority*

```python
     516:                 max_workers = policy.min_workers
     517: 
>>>  518:         return {
     519:             "max_memory_mb": max_memory,
     520:             "max_workers": max_workers,
```

#### Line 631 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
     629: 
     630:         active_strategies = [
>>>  631:             {
     632:                 "name": strategy.name,
     633:                 "threshold": strategy.pressure_threshold.value,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/signal_evidence_extractor.py

**2 violation(s)**

#### Line 369 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score = 1.0*

```python
     367:         if is_required:
     368:             # Binary: found or not
>>>  369:             score = 1.0 if found_count > 0 else 0.0
     370:         elif minimum_count > 0:
     371:             # Proportional: found / minimum, capped at 1.0
```

#### Line 375 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score = 1.0*

```python
     373:         else:
     374:             # Optional element: presence is bonus
>>>  375:             score = 1.0 if found_count > 0 else 0.5
     376: 
     377:         scores.append(score)
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/signal_fallback_fusion.py

**1 violation(s)**

#### Line 305 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: similarity_threshold*

```python
     303:             for pack in eligible_sources
     304:         ],
>>>  305:         "fusion_strategy": {
     306:             "min_source_patterns": strategy.min_source_patterns,
     307:             "max_fusion_ratio": strategy.max_fusion_ratio,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/signal_intelligence_layer.py

**1 violation(s)**

#### Line 334 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: intelligence_layer_enabled*

```python
     332:             'remediation': validation.remediation
     333:         },
>>>  334:         'metadata': {
     335:             **evidence_result.extraction_metadata,
     336:             'intelligence_layer_enabled': True,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/signal_quality_metrics.py

**5 violation(s)**

#### Line 247 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: threshold_delta=0.0*

```python
     245:             low_coverage_pas=[],
     246:             coverage_delta=0.0,
>>>  247:             threshold_delta=0.0,
     248:             gap_severity="UNKNOWN",
     249:             recommendations=["Insufficient data for gap analysis"],
```

#### Line 355 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: thresholds_calibrated*

```python
     353: 
     354:     # Quality gates
>>>  355:     quality_gates = {
     356:         "all_pas_have_patterns": all(m.pattern_count > 0 for m in metrics_by_pa.values()),
     357:         "all_pas_high_quality": len(high_quality_pas) == len(metrics_by_pa),
```

#### Line 365 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: avg_confidence_threshold, avg_evidence_threshold*

```python
     363: 
     364:     report = {
>>>  365:         "summary": {
     366:             "total_policy_areas": len(metrics_by_pa),
     367:             "total_patterns": total_patterns,
```

#### Line 378 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold_min_confidence, threshold_min_evidence*

```python
     376:         },
     377:         "by_policy_area": {
>>>  378:             pa: {
     379:                 "pattern_count": m.pattern_count,
     380:                 "indicator_count": m.indicator_count,
```

#### Line 390 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold_delta*

```python
     388:             for pa, m in metrics_by_pa.items()
     389:         },
>>>  390:         "coverage_gap_analysis": {
     391:             "high_coverage_pas": gap_analysis.high_coverage_pas,
     392:             "low_coverage_pas": gap_analysis.low_coverage_pas,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/signal_registry.py

**2 violation(s)**

#### Line 9 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: runtime validation
- OpenTelemetry for distributed tracing
- BLAKE3 for cryptogr*

```python
       7: 
       8: Technical Standards:
>>>    9: - Pydantic v2 for runtime validation
      10: - OpenTelemetry for distributed tracing
      11: - BLAKE3 for cryptographic hashing
```

#### Line 591 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'section_weights' assigned inline dict literal*

```python
     589: 
     590:         # Section weights (hardcoded calibrated values for now)
>>>  591:         section_weights = {
     592:             "DIAGNOSTICO": 0.92,
     593:             "PLAN_INVERSIONES": 1.25,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/orchestrator/versions.py

**1 violation(s)**

#### Line 81 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: calibration*

```python
      79:         Dictionary mapping component names to version strings
      80:     """
>>>   81:     return {
      82:         "pipeline": PIPELINE_VERSION,
      83:         "calibration": CALIBRATION_VERSION,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/phases/phase1_spc_ingestion_full.py

**23 violation(s)**

#### Line 34 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
      32: class Phase1MissionContract:
      33:     """
>>>   34:     CRITICAL WEIGHT: 10000
      35:     FAILURE TO MEET ANY REQUIREMENT = IMMEDIATE PIPELINE TERMINATION
      36:     NO EXCEPTIONS, NO FALLBACKS, NO PARTIAL SUCCESS
```

#### Line 42 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
      40: class PADimGridSpecification:
      41:     """
>>>   42:     WEIGHT: 10000 - NON-NEGOTIABLE GRID STRUCTURE
      43:     ANY DEVIATION = IMMEDIATE FAILURE
      44:     """
```

#### Line 75 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
      73:     def validate_chunk(cls, chunk: Any) -> None:
      74:         """
>>>   75:         HARD VALIDATION - WEIGHT: 10000
      76:         EVERY CHECK MUST PASS OR PIPELINE DIES
      77:         """
```

#### Line 111 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
     109:     def validate_chunk_set(cls, chunks: List[Any]) -> None:
     110:         """
>>>  111:         SET-LEVEL VALIDATION - WEIGHT: 10000
     112:         """
     113:         # EXACT COUNT
```

#### Line 204 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
     202: class Phase1SPCIngestionFullContract:
     203:     """
>>>  204:     CRITICAL EXECUTION CONTRACT - WEIGHT: 10000
     205:     EVERY LINE IS MANDATORY.  NO SHORTCUTS. NO ASSUMPTIONS.
     206:     """
```

#### Line 242 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 1000*

```python
     240:         """
     241:         # PRE-EXECUTION VALIDATION
>>>  242:         self._validate_canonical_input(canonical_input)  # WEIGHT: 1000
     243: 
     244:         # SUBPHASE EXECUTION - EXACT ORDER MANDATORY
```

#### Line 246 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 900*

```python
     244:         # SUBPHASE EXECUTION - EXACT ORDER MANDATORY
     245:         try:
>>>  246:             # SP0: Language Detection - WEIGHT: 900
     247:             lang_data = self._execute_sp0_language_detection(canonical_input)
     248:             self._record_subphase(0, lang_data)
```

#### Line 250 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 950*

```python
     248:             self._record_subphase(0, lang_data)
     249: 
>>>  250:             # SP1: Advanced Preprocessing - WEIGHT: 950
     251:             preprocessed = self._execute_sp1_preprocessing(canonical_input, lang_data)
     252:             self._record_subphase(1, preprocessed)
```

#### Line 254 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 950*

```python
     252:             self._record_subphase(1, preprocessed)
     253: 
>>>  254:             # SP2: Structural Analysis - WEIGHT: 950
     255:             structure = self._execute_sp2_structural(preprocessed)
     256:             self._record_subphase(2, structure)
```

#### Line 258 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 980*

```python
     256:             self._record_subphase(2, structure)
     257: 
>>>  258:             # SP3: Topic Modeling & KG - WEIGHT: 980
     259:             knowledge_graph = self._execute_sp3_knowledge_graph(preprocessed, structure)
     260:             self._record_subphase(3, knowledge_graph)
```

#### Line 262 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
     260:             self._record_subphase(3, knowledge_graph)
     261: 
>>>  262:             # SP4: PA×DIM Segmentation [CRITICAL: 60 CHUNKS] - WEIGHT: 10000
     263:             pa_dim_chunks = self._execute_sp4_segmentation(
     264:                 preprocessed, structure, knowledge_graph
```

#### Line 269 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 970*

```python
     267:             self._record_subphase(4, pa_dim_chunks)
     268: 
>>>  269:             # SP5: Causal Chain Extraction - WEIGHT: 970
     270:             causal_chains = self._execute_sp5_causal_extraction(pa_dim_chunks)
     271:             self._record_subphase(5, causal_chains)
```

#### Line 273 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 970*

```python
     271:             self._record_subphase(5, causal_chains)
     272: 
>>>  273:             # SP6: Causal Integration - WEIGHT: 970
     274:             integrated_causal = self._execute_sp6_causal_integration(
     275:                 pa_dim_chunks, causal_chains
```

#### Line 279 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 960*

```python
     277:             self._record_subphase(6, integrated_causal)
     278: 
>>>  279:             # SP7: Argumentative Analysis - WEIGHT: 960
     280:             arguments = self._execute_sp7_arguments(pa_dim_chunks, integrated_causal)
     281:             self._record_subphase(7, arguments)
```

#### Line 283 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 960*

```python
     281:             self._record_subphase(7, arguments)
     282: 
>>>  283:             # SP8: Temporal Analysis - WEIGHT: 960
     284:             temporal = self._execute_sp8_temporal(pa_dim_chunks, integrated_causal)
     285:             self._record_subphase(8, temporal)
```

#### Line 287 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 950*

```python
     285:             self._record_subphase(8, temporal)
     286: 
>>>  287:             # SP9: Discourse Analysis - WEIGHT: 950
     288:             discourse = self._execute_sp9_discourse(pa_dim_chunks, arguments)
     289:             self._record_subphase(9, discourse)
```

#### Line 291 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 990*

```python
     289:             self._record_subphase(9, discourse)
     290: 
>>>  291:             # SP10: Strategic Integration - WEIGHT: 990
     292:             strategic = self._execute_sp10_strategic(
     293:                 pa_dim_chunks, integrated_causal, arguments, temporal, discourse
```

#### Line 297 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
     295:             self._record_subphase(10, strategic)
     296: 
>>>  297:             # SP11: Smart Chunk Generation [CRITICAL: 60 CHUNKS] - WEIGHT: 10000
     298:             smart_chunks = self._execute_sp11_smart_chunks(
     299:                 pa_dim_chunks, self.subphase_results
```

#### Line 304 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 980*

```python
     302:             self._record_subphase(11, smart_chunks)
     303: 
>>>  304:             # SP12: Inter-Chunk Enrichment - WEIGHT: 980
     305:             irrigated = self._execute_sp12_irrigation(smart_chunks)
     306:             self._record_subphase(12, irrigated)
```

#### Line 308 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
     306:             self._record_subphase(12, irrigated)
     307: 
>>>  308:             # SP13: Integrity Validation [CRITICAL GATE] - WEIGHT: 10000
     309:             validated = self._execute_sp13_validation(irrigated)
     310:             self._assert_validation_pass(validated)  # HARD STOP IF FAILS
```

#### Line 313 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 970*

```python
     311:             self._record_subphase(13, validated)
     312: 
>>>  313:             # SP14: Deduplication - WEIGHT: 970
     314:             deduplicated = self._execute_sp14_deduplication(irrigated)
     315:             self._assert_chunk_count(deduplicated, 60)  # HARD STOP IF FAILS
```

#### Line 318 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 990*

```python
     316:             self._record_subphase(14, deduplicated)
     317: 
>>>  318:             # SP15: Strategic Ranking - WEIGHT: 990
     319:             ranked = self._execute_sp15_ranking(deduplicated)
     320:             self._record_subphase(15, ranked)
```

#### Line 325 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
     323:             canon_package = self._construct_cpp_with_verification(ranked)
     324: 
>>>  325:             # POSTCONDITION VERIFICATION - WEIGHT: 10000
     326:             self._verify_all_postconditions(canon_package)
     327: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/phases/phase2_models.py

**5 violation(s)**

#### Line 17 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
      15: class Phase2MissionContract:
      16:     """
>>>   17:     CRITICAL WEIGHT: 10000
      18:     PHASE 2 PROCESSES EXACTLY 300 MICRO QUESTIONS
      19:     ANY DEVIATION = IMMEDIATE PIPELINE TERMINATION
```

#### Line 32 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight*

```python
      30: 
      31:     PRIMARY_OBJECTIVES = {
>>>   32:         "QUESTION_ANSWERING": {
      33:             "requirement": "Answer ALL 300 micro questions using 60 PA×DIM chunks",
      34:             "hard_constraints": [
```

#### Line 47 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight*

```python
      45:         },
      46: 
>>>   47:         "EVIDENCE_PIPELINE": {
      48:             "requirement": "Use canonical evidence from CPP chunks",
      49:             "hard_constraints": [
```

#### Line 61 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight*

```python
      59:         },
      60: 
>>>   61:         "EXECUTION_ORDER": {
      62:             "requirement": "Dimension-first, PA-scoped processing",
      63:             "execution_sequence": [
```

#### Line 88 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: WEIGHT: 10000*

```python
      86:     """
      87:     STRICT DEFINITION OF WHAT PHASE 2 CAN ACCESS
>>>   88:     WEIGHT: 10000 - NO UNAUTHORIZED DATA ACCESS
      89:     """
      90: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/runtime_config.py

**2 violation(s)**

#### Line 222 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: ALLOW_MISSING_BASE_WEIGHTS*

```python
     220: 
     221:     # Illegal combinations in PROD mode
>>>  222:     _PROD_ILLEGAL_COMBOS: ClassVar[dict[str, tuple[str, FallbackCategory]]] = {
     223:         "ALLOW_DEV_INGESTION_FALLBACKS": (
     224:             "Development ingestion fallbacks not allowed in PROD - they bypass quality gates",
```

#### Line 416 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: missing_base_weights*

```python
     414:                 "spacy_fallback": self.allow_spacy_fallback,
     415:             },
>>>  416:             "development": {
     417:                 "dev_ingestion_fallbacks": self.allow_dev_ingestion_fallbacks,
     418:                 "aggregation_defaults": self.allow_aggregation_defaults,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/wiring/bootstrap.py

**3 violation(s)**

#### Line 45 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable '_HAS_CALIBRATION' assigned hardcoded value: True*

```python
      43:     from farfan_pipeline.core.calibration.orchestrator import CalibrationOrchestrator as _CalibrationOrchestrator
      44:     from farfan_pipeline.core.calibration.config import DEFAULT_CALIBRATION_CONFIG as _DEFAULT_CALIBRATION_CONFIG
>>>   45:     _HAS_CALIBRATION = True
      46: except Exception:  # pragma: no cover - only during stripped installs
      47:     _CalibrationOrchestrator = None  # type: ignore[assignment]
```

#### Line 49 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable '_HAS_CALIBRATION' assigned hardcoded value: False*

```python
      47:     _CalibrationOrchestrator = None  # type: ignore[assignment]
      48:     _DEFAULT_CALIBRATION_CONFIG = None  # type: ignore[assignment]
>>>   49:     _HAS_CALIBRATION = False
      50: 
      51: from farfan_pipeline.core.wiring.errors import MissingDependencyError, WiringInitializationError
```

#### Line 244 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: calibration_profile*

```python
     242:             logger.info("wiring_init_phase", phase="phase_0_validation")
     243:             phase_0_validator = Phase0Validator()
>>>  244:             raw_config = {
     245:                 "monolith_path": self.questionnaire_path,
     246:                 "questionnaire_hash": self.questionnaire_hash,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/wiring/feature_flags.py

**1 violation(s)**

#### Line 79 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: allow_threshold_override*

```python
      77:             Dictionary of flag names to values
      78:         """
>>>   79:         return {
      80:             "use_spc_ingestion": self.use_spc_ingestion,
      81:             "use_cpp_ingestion": self.use_cpp_ingestion,  # Legacy compatibility
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/wiring/validation.py

**1 violation(s)**

#### Line 166 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: aggregate->score, score->report*

```python
     164:     def __init__(self) -> None:
     165:         """Initialize wiring validator."""
>>>  166:         self._validators = {
     167:             "cpp->adapter": LinkValidator("cpp->adapter"),
     168:             "spc->adapter": LinkValidator("spc->adapter"),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/flux/cli.py

**1 violation(s)**

#### Line 56 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: runtime with assert_compat()")


def _dummy_registry_get(policy_area: str) -> di*

```python
      54:     for deliverable, expectation in contracts:
      55:         typer.echo(f"{deliverable} → {expectation}")
>>>   56:     typer.echo("\nAll contracts verified at runtime with assert_compat()")
      57: 
      58: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/flux/gates.py

**2 violation(s)**

#### Line 107 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: runtime paths.

        requires: source_paths not empty
        ensures: no YAM*

```python
     105:     def no_yaml_gate(source_paths: list[Path]) -> QualityGateResult:
     106:         """
>>>  107:         Verify no YAML files are loaded in runtime paths.
     108: 
     109:         requires: source_paths not empty
```

#### Line 251 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
     249:             gate_name="coverage",
     250:             passed=passed,
>>>  251:             details={
     252:                 "coverage": coverage_percentage,
     253:                 "threshold": threshold,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/flux/phases.py

**3 violation(s)**

#### Line 20 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: runtime_config import RuntimeConfig, get_runtime_config
from farfan_pipeline.cor*

```python
      18: 
      19: # Contract infrastructure - ACTUAL INTEGRATION
>>>   20: from farfan_pipeline.core.runtime_config import RuntimeConfig, get_runtime_config
      21: from farfan_pipeline.core.contracts.runtime_contracts import (
      22:     SegmentationMethod,
```

#### Line 1019 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: calibration*

```python
    1017:             )
    1018: 
>>> 1019:         fp = _fp({"n": df.height, "calibration": calibration})
    1020:         span.set_attribute("fingerprint", fp)
    1021:         span.set_attribute("score_count", df.height)
```

#### Line 1054 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score_count*

```python
    1052:             correlation_id=correlation_id,
    1053:             envelope_metadata=envelope_metadata or {},
>>> 1054:             metrics={"duration_ms": duration_ms, "score_count": df.height},
    1055:         )
    1056: 
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/observability/canonical_metrics/health.py

**1 violation(s)**

#### Line 32 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: calibrations_loaded*

```python
      30:     try:
      31:         if hasattr(orchestrator, 'executor'):
>>>   32:             executor_health = {
      33:                 'instances_loaded': len(orchestrator.executor.instances),
      34:                 'calibrations_loaded': len(orchestrator.executor.calibrations),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/optimization/rl_strategy.py

**1 violation(s)**

#### Line 230 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: alpha, beta*

```python
     228:     def to_dict(self) -> dict[str, Any]:
     229:         """Convert arm to dictionary."""
>>>  230:         return {
     231:             "arm_id": self.arm_id,
     232:             "name": self.name,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/processing/Copia de __init__.py

**1 violation(s)**

#### Line 240 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: quality_score*

```python
     238:         # Quality gate: Validate chunks
     239:         chunk_dicts = [
>>>  240:             {
     241:                 "text": c.text,
     242:                 "chunk_id": c.chunk_id,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/processing/aggregation.py

**24 violation(s)**

#### Line 341 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
     339:     """
     340:     validated_results = []
>>>  341:     required_keys = {
     342:         "question_global": int, "base_slot": str, "policy_area": str, "dimension": str,
     343:         "score": float, "quality_level": str, "evidence": dict, "raw_results": dict
```

#### Line 606 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight_sum:.6*

```python
     604:         if abs(weight_sum - ParameterLoaderV2.get("farfan_core.processing.aggregation.DimensionAggregator.validate_weights", "auto_param_L603_28", 1.0)) > tolerance:
     605:             expected_weight = ParameterLoaderV2.get("farfan_core.processing.aggregation.DimensionAggregator.validate_weights", "auto_param_L604_81", 1.0)
>>>  606:             msg = f"Weight sum validation failed: sum={weight_sum:.6f}, expected={expected_weight}"
     607:             logger.error(msg)
     608:             if self.abort_on_insufficient:
```

#### Line 612 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight_sum:.6*

```python
     610:             return False, msg
     611: 
>>>  612:         logger.debug(f"Weight validation passed: sum={weight_sum:.6f}")
     613:         return True, "Weights valid"
     614: 
```

#### Line 694 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weighted_sum:.4*

```python
     692:         logger.debug(
     693:             f"Weighted average calculated: "
>>>  694:             f"scores={scores}, weights={weights}, result={weighted_sum:.4f}"
     695:         )
     696: 
```

#### Line 742 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.4*

```python
     740: 
     741:         logger.debug(
>>>  742:             f"Rubric applied: score={score:.4f}, "
     743:             f"normalized={normalized_score:.4f}, quality={quality}"
     744:         )
```

#### Line 743 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: normalized_score:.4*

```python
     741:         logger.debug(
     742:             f"Rubric applied: score={score:.4f}, "
>>>  743:             f"normalized={normalized_score:.4f}, quality={quality}"
     744:         )
     745: 
```

#### Line 823 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weights, score*

```python
     821:         try:
     822:             avg_score = self.calculate_weighted_average(scores, resolved_weights)
>>>  823:             validation_details["weights"] = {
     824:                 "valid": True,
     825:                 "weights": resolved_weights if resolved_weights else "equal",
```

#### Line 842 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
     840:         # Apply rubric thresholds
     841:         quality_level = self.apply_rubric_thresholds(avg_score)
>>>  842:         validation_details["rubric"] = {
     843:             "score": avg_score,
     844:             "quality_level": quality_level
```

#### Line 851 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: avg_score:.4*

```python
     849:         logger.info(
     850:             f"✓ Dimension {dimension_id}/{area_id}: "
>>>  851:             f"score={avg_score:.4f}, quality={quality_level}"
     852:         )
     853: 
```

#### Line 1198 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.4*

```python
    1196: 
    1197:         logger.debug(
>>> 1198:             f"Area rubric applied: score={score:.4f}, "
    1199:             f"normalized={normalized_score:.4f}, quality={quality}"
    1200:         )
```

#### Line 1199 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: normalized_score:.4*

```python
    1197:         logger.debug(
    1198:             f"Area rubric applied: score={score:.4f}, "
>>> 1199:             f"normalized={normalized_score:.4f}, quality={quality}"
    1200:         )
    1201: 
```

#### Line 1289 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
    1287:         # Apply rubric thresholds
    1288:         quality_level = self.apply_rubric_thresholds(avg_score)
>>> 1289:         validation_details["rubric"] = {
    1290:             "score": avg_score,
    1291:             "quality_level": quality_level
```

#### Line 1303 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: avg_score:.4*

```python
    1301:         logger.info(
    1302:             f"✓ Policy area {area_id} ({area_name}): "
>>> 1303:             f"score={avg_score:.4f}, quality={quality_level}"
    1304:         )
    1305: 
```

#### Line 1381 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'MAX_SCORE' assigned hardcoded value: 3.0*

```python
    1379: 
    1380:     PENALTY_WEIGHT = ParameterLoaderV2.get("farfan_core.processing.aggregation.AreaPolicyAggregator.normalize_scores", "PENALTY_WEIGHT", 0.3)
>>> 1381:     MAX_SCORE = 3.0
    1382: 
    1383:     def __init__(
```

#### Line 1381 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: MAX_SCORE = 3.0*

```python
    1379: 
    1380:     PENALTY_WEIGHT = ParameterLoaderV2.get("farfan_core.processing.aggregation.AreaPolicyAggregator.normalize_scores", "PENALTY_WEIGHT", 0.3)
>>> 1381:     MAX_SCORE = 3.0
    1382: 
    1383:     def __init__(
```

#### Line 1513 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight_sum:.6*

```python
    1511:         tolerance = 1e-6
    1512:         if abs(weight_sum - ParameterLoaderV2.get("farfan_core.processing.aggregation.AreaPolicyAggregator.normalize_scores", "auto_param_L1510_28", 1.0)) > tolerance:
>>> 1513:             msg = f"Cluster weight validation failed: sum={weight_sum:.6f}"
    1514:             logger.error(msg)
    1515:             if self.abort_on_insufficient:
```

#### Line 1523 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weighted_avg:.4*

```python
    1521:         logger.debug(
    1522:             f"Cluster weights applied: scores={scores}, "
>>> 1523:             f"weights={weights}, result={weighted_avg:.4f}"
    1524:         )
    1525: 
```

#### Line 1661 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weights, score*

```python
    1659:         try:
    1660:             weighted_score = self.apply_cluster_weights(cluster_area_scores, resolved_weights)
>>> 1661:             validation_details["weights"] = {
    1662:                 "valid": True,
    1663:                 "weights": resolved_weights if resolved_weights else "equal",
```

#### Line 1703 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: raw_score, adjusted_score*

```python
    1701:         if weakest_area:
    1702:             validation_details["weakest_area"] = weakest_area.area_id
>>> 1703:         validation_details["imbalance_penalty"] = {
    1704:             "std_dev": std_dev,
    1705:             "penalty_factor": penalty_factor,
```

#### Line 1712 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: adjusted_score:.4*

```python
    1710:         logger.info(
    1711:             f"✓ Cluster {cluster_id} ({cluster_name}): "
>>> 1712:             f"score={adjusted_score:.4f}, coherence={coherence:.4f}"
    1713:         )
    1714: 
```

#### Line 1969 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score:.4*

```python
    1967: 
    1968:         logger.debug(
>>> 1969:             f"Macro rubric applied: score={score:.4f}, "
    1970:             f"normalized={normalized_score:.4f}, quality={quality}"
    1971:         )
```

#### Line 1970 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: normalized_score:.4*

```python
    1968:         logger.debug(
    1969:             f"Macro rubric applied: score={score:.4f}, "
>>> 1970:             f"normalized={normalized_score:.4f}, quality={quality}"
    1971:         )
    1972: 
```

#### Line 2037 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: score*

```python
    2035:         # Apply quality rubric
    2036:         quality_level = self.apply_rubric_thresholds(macro_score)
>>> 2037:         validation_details["rubric"] = {
    2038:             "score": macro_score,
    2039:             "quality_level": quality_level
```

#### Line 2043 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: macro_score:.4*

```python
    2041: 
    2042:         logger.info(
>>> 2043:             f"✓ Macro evaluation (Q305): score={macro_score:.4f}, "
    2044:             f"quality={quality_level}, coherence={cross_cutting_coherence:.4f}, "
    2045:             f"alignment={strategic_alignment:.4f}, gaps={len(systemic_gaps)}"
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/processing/converter.py

**1 violation(s)**

#### Line 596 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: coherence_score, actionability_score*

```python
     594: 
     595:         for sc in smart_chunks:
>>>  596:             chunk_data = {
     597:                 'chunk_id': sc.chunk_id,
     598:                 'semantic_density': sc.semantic_density,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/processing/embedding_policy.py

**1 violation(s)**

#### Line 1197 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: relevance_score*

```python
    1195:         # Extract key evidence passages
    1196:         evidence_passages = [
>>> 1197:             {
    1198:                 "content": chunk["content"][:300],
    1199:                 "relevance_score": float(score),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/processing/policy_processor.py

**10 violation(s)**

#### Line 33 - `INLINE_CALIBRATION_DICT` [HIGH]

*Pattern matched: runtime error fixes for defensive programming
from farfan_pipeline.utils.runtime*

```python
      31: import numpy as np
      32: 
>>>   33: # Import runtime error fixes for defensive programming
      34: from farfan_pipeline.utils.runtime_error_fixes import ensure_list_return
      35: 
```

#### Line 344 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold*

```python
     342:     )
     343: 
>>>  344:     LEGACY_PARAM_MAP: ClassVar[dict[str, str]] = {
     345:         "keep_structure": "preserve_document_structure",
     346:         "tag_elements": "enable_semantic_tagging",
```

#### Line 878 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: bayesian_scores*

```python
     876:         except PDETAnalysisException as exc:
     877:             logger.error("Contradiction analysis failed: %s", exc)
>>>  878:             contradiction_bundle = {
     879:                 "reports": {},
     880:                 "temporal_assessments": {},
```

#### Line 900 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: bayesian_dimension_scores, quality_score*

```python
     898: 
     899:         # Compile results
>>>  900:         return {
     901:             "metadata": metadata,
     902:             "point_evidence": point_evidence,
```

#### Line 919 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: confidence_threshold*

```python
     917:             },
     918:             "processing_status": "complete",
>>>  919:             "config_snapshot": {
     920:                 "confidence_threshold": self.config.confidence_threshold,
     921:                 "bayesian_enabled": self.config.enable_bayesian_scoring,
```

#### Line 1020 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'domain_weights' assigned inline dict literal*

```python
    1018:         }
    1019: 
>>> 1020:         domain_weights = {
    1021:             CausalDimension.D1_INSUMOS: 1.1,
    1022:             CausalDimension.D2_ACTIVIDADES: ParameterLoaderV2.get("farfan_core.processing.policy_processor.IndustrialPolicyProcessor.process", "auto_param_L1000_44", 1.0),
```

#### Line 1085 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: criticality_score*

```python
    1083: 
    1084:                 severity = 1 - coherence_score if coherence_score else ParameterLoaderV2.get("farfan_core.processing.policy_processor.IndustrialPolicyProcessor.process", "auto_param_L1062_71", 0.5)
>>> 1085:                 critical_links[dimension.value] = {
    1086:                     "criticality_score": round(min(ParameterLoaderV2.get("farfan_core.processing.policy_processor.IndustrialPolicyProcessor.process", "auto_param_L1064_51", 1.0), max(ParameterLoaderV2.get("farfan_core.processing.policy_processor.IndustrialPolicyProcessor.process", "auto_param_L1064_60", 0.0), severity)), 4),
    1087:                     "text_analysis": {
```

#### Line 1101 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: bayesian_scores*

```python
    1099:                 )
    1100: 
>>> 1101:         return {
    1102:             "reports": reports,
    1103:             "temporal_assessments": temporal_assessments,
```

#### Line 1159 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: bayesian_scores*

```python
    1157:         )
    1158: 
>>> 1159:         evidence = {
    1160:             "bayesian_scores": bayesian_scores,
    1161:             "dimension_confidences": {
```

#### Line 1247 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'dimension_scores' assigned inline dict literal*

```python
    1245:             sentences = self.text_processor.segment_into_sentences(text)
    1246: 
>>> 1247:         dimension_scores = {}
    1248: 
    1249:         for dimension, categories in self._pattern_registry.items():
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/processing/quality_gates.py

**5 violation(s)**

#### Line 27 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'MIN_STRATEGIC_SCORE' assigned hardcoded value: 0.3*

```python
      25:     MIN_CHUNK_LENGTH = 50  # characters
      26:     MAX_CHUNK_LENGTH = 5000
>>>   27:     MIN_STRATEGIC_SCORE = 0.3
      28:     MIN_QUALITY_SCORE = 0.5
      29:     REQUIRED_CHUNK_FIELDS = ['text', 'chunk_id', 'strategic_importance', 'quality_score']
```

#### Line 27 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: MIN_STRATEGIC_SCORE = 0.3*

```python
      25:     MIN_CHUNK_LENGTH = 50  # characters
      26:     MAX_CHUNK_LENGTH = 5000
>>>   27:     MIN_STRATEGIC_SCORE = 0.3
      28:     MIN_QUALITY_SCORE = 0.5
      29:     REQUIRED_CHUNK_FIELDS = ['text', 'chunk_id', 'strategic_importance', 'quality_score']
```

#### Line 28 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'MIN_QUALITY_SCORE' assigned hardcoded value: 0.5*

```python
      26:     MAX_CHUNK_LENGTH = 5000
      27:     MIN_STRATEGIC_SCORE = 0.3
>>>   28:     MIN_QUALITY_SCORE = 0.5
      29:     REQUIRED_CHUNK_FIELDS = ['text', 'chunk_id', 'strategic_importance', 'quality_score']
      30: 
```

#### Line 28 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: MIN_QUALITY_SCORE = 0.5*

```python
      26:     MAX_CHUNK_LENGTH = 5000
      27:     MIN_STRATEGIC_SCORE = 0.3
>>>   28:     MIN_QUALITY_SCORE = 0.5
      29:     REQUIRED_CHUNK_FIELDS = ['text', 'chunk_id', 'strategic_importance', 'quality_score']
      30: 
```

#### Line 210 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: budget_consistency_score*

```python
     208: 
     209:         # Store actual values
>>>  210:         metrics_dict = {
     211:             'provenance_completeness': provenance_completeness,
     212:             'structural_consistency': structural_consistency,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/processing/semantic_chunking_policy.py

**2 violation(s)**

#### Line 365 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: posterior_mean, posterior_std*

```python
     363:         max_entropy = stats.beta.entropy(1, 1)  # Maximum uncertainty
     364:         confidence = ParameterLoaderV2.get("farfan_core.processing.semantic_chunking_policy.BayesianEvidenceIntegrator.__init__", "auto_param_L366_21", 1.0) - (posterior_entropy / max_entropy)
>>>  365:         return {
     366:             "posterior_mean": float(np.clip(posterior_mean, ParameterLoaderV2.get("farfan_core.processing.semantic_chunking_policy.BayesianEvidenceIntegrator.__init__", "auto_param_L368_60", 0.0), ParameterLoaderV2.get("farfan_core.processing.semantic_chunking_policy.BayesianEvidenceIntegrator.__init__", "auto_param_L368_65", 1.0))),
     367:             "posterior_std": float(np.sqrt(posterior_variance)),
```

#### Line 423 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: posterior_mean, posterior_std*

```python
     421:         prior_var = self.prior_alpha / \
     422:             ((2 * self.prior_alpha)**2 * (2 * self.prior_alpha + 1))
>>>  423:         return {
     424:             "posterior_mean": prior_mean,
     425:             "posterior_std": float(np.sqrt(prior_var)),
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/processing/spc_ingestion.py

**27 violation(s)**

#### Line 338 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'SEMANTIC_COHERENCE_THRESHOLD' assigned hardcoded value: 0.72*

```python
     336: 
     337:     # Umbrales semánticos
>>>  338:     SEMANTIC_COHERENCE_THRESHOLD = 0.72
     339:     CROSS_REFERENCE_MIN_SIMILARITY = 0.65
     340:     CAUSAL_CHAIN_MIN_CONFIDENCE = 0.60
```

#### Line 338 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: SEMANTIC_COHERENCE_THRESHOLD = 0.72*

```python
     336: 
     337:     # Umbrales semánticos
>>>  338:     SEMANTIC_COHERENCE_THRESHOLD = 0.72
     339:     CROSS_REFERENCE_MIN_SIMILARITY = 0.65
     340:     CAUSAL_CHAIN_MIN_CONFIDENCE = 0.60
```

#### Line 341 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'ENTITY_EXTRACTION_THRESHOLD' assigned hardcoded value: 0.55*

```python
     339:     CROSS_REFERENCE_MIN_SIMILARITY = 0.65
     340:     CAUSAL_CHAIN_MIN_CONFIDENCE = 0.60
>>>  341:     ENTITY_EXTRACTION_THRESHOLD = 0.55
     342: 
     343:     # Parámetros de ventana de contexto
```

#### Line 341 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: ENTITY_EXTRACTION_THRESHOLD = 0.55*

```python
     339:     CROSS_REFERENCE_MIN_SIMILARITY = 0.65
     340:     CAUSAL_CHAIN_MIN_CONFIDENCE = 0.60
>>>  341:     ENTITY_EXTRACTION_THRESHOLD = 0.55
     342: 
     343:     # Parámetros de ventana de contexto
```

#### Line 351 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'HIERARCHICAL_CLUSTER_THRESHOLD' assigned hardcoded value: 0.7*

```python
     349:     DBSCAN_EPS = 0.25
     350:     DBSCAN_MIN_SAMPLES = 2
>>>  351:     HIERARCHICAL_CLUSTER_THRESHOLD = 0.70
     352: 
     353:     # Análisis causal
```

#### Line 351 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: HIERARCHICAL_CLUSTER_THRESHOLD = 0.70*

```python
     349:     DBSCAN_EPS = 0.25
     350:     DBSCAN_MIN_SAMPLES = 2
>>>  351:     HIERARCHICAL_CLUSTER_THRESHOLD = 0.70
     352: 
     353:     # Análisis causal
```

#### Line 364 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'MIN_COHERENCE_SCORE' assigned hardcoded value: 0.55*

```python
     362:     # Métricas de calidad
     363:     MIN_INFORMATION_DENSITY = 0.40
>>>  364:     MIN_COHERENCE_SCORE = 0.55
     365:     MIN_COMPLETENESS_INDEX = 0.60
     366:     MIN_STRATEGIC_IMPORTANCE = 0.45
```

#### Line 364 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: MIN_COHERENCE_SCORE = 0.55*

```python
     362:     # Métricas de calidad
     363:     MIN_INFORMATION_DENSITY = 0.40
>>>  364:     MIN_COHERENCE_SCORE = 0.55
     365:     MIN_COMPLETENESS_INDEX = 0.60
     366:     MIN_STRATEGIC_IMPORTANCE = 0.45
```

#### Line 369 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'DEDUPLICATION_THRESHOLD' assigned hardcoded value: 0.88*

```python
     367: 
     368:     # Deduplicación
>>>  369:     DEDUPLICATION_THRESHOLD = 0.88
     370:     NEAR_DUPLICATE_THRESHOLD = 0.92 #
     371: 
```

#### Line 369 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: DEDUPLICATION_THRESHOLD = 0.88*

```python
     367: 
     368:     # Deduplicación
>>>  369:     DEDUPLICATION_THRESHOLD = 0.88
     370:     NEAR_DUPLICATE_THRESHOLD = 0.92 #
     371: 
```

#### Line 370 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'NEAR_DUPLICATE_THRESHOLD' assigned hardcoded value: 0.92*

```python
     368:     # Deduplicación
     369:     DEDUPLICATION_THRESHOLD = 0.88
>>>  370:     NEAR_DUPLICATE_THRESHOLD = 0.92 #
     371: 
     372: # =============================================================================
```

#### Line 370 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: NEAR_DUPLICATE_THRESHOLD = 0.92*

```python
     368:     # Deduplicación
     369:     DEDUPLICATION_THRESHOLD = 0.88
>>>  370:     NEAR_DUPLICATE_THRESHOLD = 0.92 #
     371: 
     372: # =============================================================================
```

#### Line 413 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: topic_alignment*

```python
     411:             offset = end
     412: 
>>>  413:             segment = {
     414:                 "text": ch_text,
     415:                 "context": ch_text,  # Can expand context if needed
```

#### Line 769 - `UNDECLARED_BAYESIAN_PRIOR` [MEDIUM]

*Potential undeclared Bayesian prior: LatentDirichletAllocation()*

```python
     767:         self.logger = logging.getLogger(self.__class__.__name__)
     768:         self.tfidf_vectorizer = TfidfVectorizer(stop_words=self.parent._get_stopwords(), ngram_range=(1, 2), max_df=0.85, min_df=2)
>>>  769:         self.lda_model = LatentDirichletAllocation(n_components=self.parent.config.N_TOPICS_LDA, random_state=42)
     770: 
     771:     def _get_stopwords(self) -> List[str]:
```

#### Line 794 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: weight*

```python
     792:                 top_features = [(feature_names[i], topic[i]) for i in top_features_ind]
     793: 
>>>  794:                 topics.append({
     795:                     'topic_id': topic_idx,
     796:                     'keywords': top_features,
```

#### Line 1060 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'score' assigned hardcoded value: 0.0*

```python
    1058:         """Calcular la coherencia de los marcadores temporales"""
    1059:         # Simple métrica basada en la presencia de orden y hitos
>>> 1060:         score = 0.0
    1061:         if flow:
    1062:             score += 0.5
```

#### Line 1060 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: score = 0.0*

```python
    1058:         """Calcular la coherencia de los marcadores temporales"""
    1059:         # Simple métrica basada en la presencia de orden y hitos
>>> 1060:         score = 0.0
    1061:         if flow:
    1062:             score += 0.5
```

#### Line 1117 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: complexity_score*

```python
    1115:         info_flow = self.parent._analyze_information_flow(full_text)
    1116: 
>>> 1117:         return {
    1118:             'coherence_relations': relations[:10],
    1119:             'rhetorical_moves': list(rhetorical.keys()),
```

#### Line 2118 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'strength_score' assigned hardcoded value: 0.5*

```python
    2116:     def _calculate_causal_strength(self, match_text: str, context: str) -> float:
    2117:         """Calcular fuerza de relación causal"""
>>> 2118:         strength_score = 0.5
    2119: 
    2120:         # Reforzadores (Boosters)
```

#### Line 2118 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: strength_score = 0.5*

```python
    2116:     def _calculate_causal_strength(self, match_text: str, context: str) -> float:
    2117:         """Calcular fuerza de relación causal"""
>>> 2118:         strength_score = 0.5
    2119: 
    2120:         # Reforzadores (Boosters)
```

#### Line 2446 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'weights' assigned inline dict literal*

```python
    2444:         """Calcular métricas de confianza y calidad"""
    2445: 
>>> 2446:         weights = {
    2447:             'causal': 0.4,
    2448:             'entity': 0.3,
```

#### Line 2553 - `HARDCODED_CALIBRATION_VALUE` [HIGH]

*Variable 'topic_score' assigned hardcoded value: 0*

```python
    2551: 
    2552:         for topic in global_topics.get('topics', []):
>>> 2553:             topic_score = 0
    2554:             for keyword, _ in topic['keywords'][:10]:
    2555:                 if keyword.lower() in text_lower:
```

#### Line 2553 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: topic_score = 0*

```python
    2551: 
    2552:         for topic in global_topics.get('topics', []):
>>> 2553:             topic_score = 0
    2554:             for keyword, _ in topic['keywords'][:10]:
    2555:                 if keyword.lower() in text_lower:
```

#### Line 2633 - `INLINE_CALIBRATION_DICT` [HIGH]

*Variable 'scores' assigned inline dict literal*

```python
    2631:         }
    2632: 
>>> 2633:         scores = {}
    2634:         for chunk_type, indicators in type_indicators.items():
    2635:             score = sum(1 for ind in indicators if ind in text_lower)
```

#### Line 3040 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: relevance_score*

```python
    3038:         relevance_score = float(np.mean(similarities[top_indices])) if len(top_indices) > 0 else 0.0
    3039: 
>>> 3040:         return {
    3041:             "text": segment_text,
    3042:             "position": (segment_start, segment_end),
```

#### Line 3342 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: position_weight*

```python
    3340:     ) -> float:
    3341:         """Evaluar importancia estratégica"""
>>> 3342:         factors = {
    3343:             'causal_strength': np.mean([e.strength_score for e in causal_evidence]) if causal_evidence else 0,
    3344:             'entity_relevance': len([e for e in policy_entities if e.context_role in [PolicyEntityRole.EXECUTOR, PolicyEntityRole.BENEFICIARY]]) / max(len(policy_entities), 1),
```

#### Line 3625 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: semantic_coherence_threshold*

```python
    3623:         output_data = {
    3624:             'metadata': metadata,
>>> 3625:             'config': {
    3626:                 'min_chunk_size': chunking_system.config.MIN_CHUNK_SIZE,
    3627:                 'max_chunk_size': chunking_system.config.MAX_CHUNK_SIZE,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/utils/coverage_gate.py

**1 violation(s)**

#### Line 108 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: threshold, meets_threshold*

```python
     106:         "files": {},
     107:         "producers": {},
>>>  108:         "totals": {
     109:             "file_public_methods": 0,
     110:             "file_total_methods": 0,
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/utils/cpp_adapter.py

**1 violation(s)**

#### Line 536 - `INLINE_CALIBRATION_DICT` [HIGH]

*Dict literal contains calibration keys: budget_consistency_score*

```python
     534:         if hasattr(canon_package, "quality_metrics") and canon_package.quality_metrics:
     535:             qm = canon_package.quality_metrics
>>>  536:             metadata_dict["quality_metrics"] = {
     537:                 "provenance_completeness": (
     538:                     qm.provenance_completeness
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/utils/metadata_loader.py

**6 violation(s)**

#### Line 184 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yaml'*

```python
     182:             if path.suffix in ['.json']:
     183:                 return json.loads(content)
>>>  184:             elif path.suffix in ['.yaml', '.yml']:
     185:                 return yaml.safe_load(content)
     186:             else:
```

#### Line 184 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yml'*

```python
     182:             if path.suffix in ['.json']:
     183:                 return json.loads(content)
>>>  184:             elif path.suffix in ['.yaml', '.yml']:
     185:                 return yaml.safe_load(content)
     186:             else:
```

#### Line 189 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .YAML*

```python
     187:                 raise ValueError(f"Unsupported file type: {path.suffix}")
     188: 
>>>  189:         except (json.JSONDecodeError, yaml.YAMLError) as e:
     190:             raise MetadataError(f"Failed to parse {path}: {e}")
     191: 
```

#### Line 271 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yaml*

```python
     269: ) -> dict[str, Any]:
     270:     """
>>>  271:     Load and validate execution_mapping.yaml
     272: 
     273:     Args:
```

#### Line 274 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yaml*

```python
     272: 
     273:     Args:
>>>  274:         path: Path to execution mapping (default: execution_mapping.yaml)
     275:         required_version: Required version
     276: 
```

#### Line 281 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yaml"*

```python
     279:     """
     280:     if path is None:
>>>  281:         path = proj_root() / "execution_mapping.yaml"
     282: 
     283:     loader = MetadataLoader()
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/utils/paths.py

**2 violation(s)**

#### Line 310 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yaml"*

```python
     308: 
     309:     Example:
>>>  310:         >>> resources("farfan_core.core", "config", "default.yaml")
     311:         Path('/path/to/farfan_core/core/config/default.yaml')
     312:     """
```

#### Line 311 - `YAML_REFERENCE` [HIGH]

*Pattern matched: .yaml'*

```python
     309:     Example:
     310:         >>> resources("farfan_core.core", "config", "default.yaml")
>>>  311:         Path('/path/to/farfan_core/core/config/default.yaml')
     312:     """
     313:     try:
```

### /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/utils/validation/aggregation_models.py

**1 violation(s)**

#### Line 55 - `HARDCODED_CALIBRATION_VALUE` [MEDIUM]

*Pattern matched: weight_sum:.6*

```python
      53:         if diff > self.tolerance:
      54:             raise ValueError(
>>>   55:                 f"Weight sum validation failed: sum={weight_sum:.6f}, expected={expected_sum}. "
      56:                 f"Difference {diff:.6f} exceeds tolerance {self.tolerance:.6f}."
      57:             )
```

## YAML File References (PROHIBITED)

**CRITICAL**: YAML is a prohibited format for calibration data.

- /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/derek_beach.py
- /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/analysis/factory.py
- /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/core/method_inventory.py
- /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/utils/metadata_loader.py
- /Users/recovered/Library/Application Support/Tonkotsu/tasks/F.A.R.F.A.N-MECHANISTIC_POLICY_PIPELINE_FINAL_RyToiHebPMBJL9KUCveB4/src/farfan_pipeline/utils/paths.py

## Remediation Recommendations

1. **Move all calibration values to JSON config files**:
   - `config/intrinsic_calibration.json` for @b scores
   - `config/contextual_parametrization.json` for layer parameters

2. **Remove inline dict/JSON literals**:
   - Load all calibration data via `IntrinsicCalibrationLoader`
   - Use `CalibrationOrchestrator` as single entry point

3. **Eliminate YAML references**:
   - Convert any YAML files to JSON
   - Update all file references

4. **Declare Bayesian priors explicitly**:
   - Document all priors in calibration config
   - Add prior justification comments

5. **Use CalibrationOrchestrator exclusively**:
   - Remove direct score computations
   - Route all calibration through `calibrate_method()`

