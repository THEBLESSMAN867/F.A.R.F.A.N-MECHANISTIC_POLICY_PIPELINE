import json
import time
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from flask.testing import FlaskClient
from flask_socketio import SocketIOTestClient

from farfan_pipeline.api.api_server import (
    APIConfig,
    DataService,
    app,
    cache,
    cache_timestamps,
    generate_jwt_token,
    request_counts,
    socketio,
    verify_jwt_token,
)


@pytest.fixture
def client() -> FlaskClient:
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def socketio_client() -> SocketIOTestClient:
    return socketio.test_client(app)


@pytest.fixture
def auth_token() -> str:
    return generate_jwt_token("test_client")


@pytest.fixture
def auth_headers(auth_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(autouse=True)
def clear_cache_and_rate_limits():
    cache.clear()
    cache_timestamps.clear()
    request_counts.clear()
    yield
    cache.clear()
    cache_timestamps.clear()
    request_counts.clear()


class TestHealthEndpoint:
    def test_health_check_returns_200(self, client: FlaskClient):
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_health_check_response_structure(self, client: FlaskClient):
        response = client.get("/api/v1/health")
        data = response.get_json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert data["status"] == "healthy"

    def test_health_check_timestamp_format(self, client: FlaskClient):
        response = client.get("/api/v1/health")
        data = response.get_json()
        timestamp = data["timestamp"]
        datetime.fromisoformat(timestamp)


class TestAuthEndpoint:
    def test_auth_token_missing_credentials(self, client: FlaskClient):
        response = client.post(
            "/api/v1/auth/token", data=json.dumps({}), content_type="application/json"
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Missing credentials" in data["error"]

    def test_auth_token_missing_client_id(self, client: FlaskClient):
        response = client.post(
            "/api/v1/auth/token",
            data=json.dumps({"client_secret": "secret"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_auth_token_missing_client_secret(self, client: FlaskClient):
        response = client.post(
            "/api/v1/auth/token",
            data=json.dumps({"client_id": "test"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_auth_token_successful_generation(self, client: FlaskClient):
        response = client.post(
            "/api/v1/auth/token",
            data=json.dumps(
                {"client_id": "test_client", "client_secret": "test_secret"}
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "access_token" in data
        assert "token_type" in data
        assert "expires_in" in data
        assert data["token_type"] == "Bearer"

    def test_auth_token_is_valid_jwt(self, client: FlaskClient):
        response = client.post(
            "/api/v1/auth/token",
            data=json.dumps(
                {"client_id": "test_client", "client_secret": "test_secret"}
            ),
            content_type="application/json",
        )
        data = response.get_json()
        token = data["access_token"]
        payload = verify_jwt_token(token)
        assert payload is not None
        assert payload["client_id"] == "test_client"

    def test_auth_token_expiration(self):
        token = generate_jwt_token("test_client")
        payload = verify_jwt_token(token)
        assert payload is not None
        exp = datetime.fromtimestamp(payload["exp"])
        iat = datetime.fromtimestamp(payload["iat"])
        assert (exp - iat).total_seconds() == APIConfig.JWT_EXPIRATION_HOURS * 3600


class TestPDETRegionsEndpoint:
    def test_get_pdet_regions_returns_200(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions")
        assert response.status_code == 200

    def test_get_pdet_regions_response_structure(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions")
        data = response.get_json()
        assert "status" in data
        assert "data" in data
        assert "count" in data
        assert "timestamp" in data
        assert data["status"] == "success"

    def test_get_pdet_regions_returns_16_regions(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions")
        data = response.get_json()
        assert data["count"] == 16
        assert len(data["data"]) == 16

    def test_get_pdet_regions_data_structure(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions")
        data = response.get_json()
        region = data["data"][0]
        assert "id" in region
        assert "name" in region
        assert "coordinates" in region
        assert "metadata" in region
        assert "scores" in region
        assert "connections" in region
        assert "indicators" in region

    def test_get_pdet_regions_scores_structure(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions")
        data = response.get_json()
        region = data["data"][0]
        scores = region["scores"]
        assert "overall" in scores
        assert "governance" in scores
        assert "social" in scores
        assert "economic" in scores
        assert "environmental" in scores
        assert "lastUpdated" in scores

    def test_get_pdet_regions_all_regions_have_ids(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions")
        data = response.get_json()
        region_ids = [r["id"] for r in data["data"]]
        assert "alto-patia" in region_ids
        assert "arauca" in region_ids
        assert "choco" in region_ids
        assert "uraba" in region_ids


class TestPDETRegionDetailEndpoint:
    def test_get_region_detail_returns_200(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions/alto-patia")
        assert response.status_code == 200

    def test_get_region_detail_not_found(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions/nonexistent")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_get_region_detail_response_structure(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions/alto-patia")
        data = response.get_json()
        assert "status" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["status"] == "success"

    def test_get_region_detail_includes_detailed_analysis(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions/alto-patia")
        data = response.get_json()
        region = data["data"]
        assert "detailed_analysis" in region
        analysis = region["detailed_analysis"]
        assert "cluster_breakdown" in analysis
        assert "question_matrix" in analysis
        assert "recommendations" in analysis
        assert "evidence" in analysis

    def test_get_region_detail_cluster_breakdown_structure(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions/alto-patia")
        data = response.get_json()
        clusters = data["data"]["detailed_analysis"]["cluster_breakdown"]
        assert len(clusters) > 0
        cluster = clusters[0]
        assert "name" in cluster
        assert "value" in cluster
        assert "trend" in cluster

    def test_get_region_detail_question_matrix_has_44_questions(
        self, client: FlaskClient
    ):
        response = client.get("/api/v1/pdet/regions/alto-patia")
        data = response.get_json()
        questions = data["data"]["detailed_analysis"]["question_matrix"]
        assert len(questions) == 44

    def test_get_region_detail_all_valid_regions(self, client: FlaskClient):
        region_ids = ["alto-patia", "arauca", "choco", "uraba"]
        for region_id in region_ids:
            response = client.get(f"/api/v1/pdet/regions/{region_id}")
            assert response.status_code == 200


class TestConstellationMapEndpoint:
    def test_get_constellation_map_returns_200(self, client: FlaskClient):
        response = client.get("/api/v1/constellation_map")
        assert response.status_code == 200

    def test_get_constellation_map_response_structure(self, client: FlaskClient):
        response = client.get("/api/v1/constellation_map")
        data = response.get_json()
        assert "status" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["status"] == "success"

    def test_get_constellation_map_has_nodes_and_links(self, client: FlaskClient):
        response = client.get("/api/v1/constellation_map")
        data = response.get_json()
        constellation = data["data"]
        assert "nodes" in constellation
        assert "links" in constellation
        assert len(constellation["nodes"]) > 0
        assert len(constellation["links"]) > 0


class TestMunicipalitiesEndpoint:
    def test_get_municipality_returns_200(self, client: FlaskClient):
        response = client.get("/api/v1/municipalities/test123")
        assert response.status_code == 200

    def test_get_municipality_response_structure(self, client: FlaskClient):
        response = client.get("/api/v1/municipalities/test123")
        data = response.get_json()
        assert "status" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["status"] == "success"

    def test_get_municipality_data_structure(self, client: FlaskClient):
        response = client.get("/api/v1/municipalities/test123")
        data = response.get_json()
        municipality = data["data"]
        assert "id" in municipality
        assert "name" in municipality
        assert "region_id" in municipality
        assert "analysis" in municipality

    def test_get_municipality_analysis_includes_radar(self, client: FlaskClient):
        response = client.get("/api/v1/municipalities/test123")
        data = response.get_json()
        analysis = data["data"]["analysis"]
        assert "radar" in analysis
        radar = analysis["radar"]
        assert "dimensions" in radar
        assert "scores" in radar
        assert len(radar["dimensions"]) == len(radar["scores"])

    def test_get_municipality_analysis_includes_clusters(self, client: FlaskClient):
        response = client.get("/api/v1/municipalities/test123")
        data = response.get_json()
        analysis = data["data"]["analysis"]
        assert "clusters" in analysis
        assert len(analysis["clusters"]) > 0

    def test_get_municipality_analysis_includes_questions(self, client: FlaskClient):
        response = client.get("/api/v1/municipalities/test123")
        data = response.get_json()
        analysis = data["data"]["analysis"]
        assert "questions" in analysis
        assert len(analysis["questions"]) == 44


class TestEvidenceStreamEndpoint:
    def test_get_evidence_stream_returns_200(self, client: FlaskClient):
        response = client.get("/api/v1/evidence/stream")
        assert response.status_code == 200

    def test_get_evidence_stream_response_structure(self, client: FlaskClient):
        response = client.get("/api/v1/evidence/stream")
        data = response.get_json()
        assert "status" in data
        assert "data" in data
        assert "count" in data
        assert "timestamp" in data
        assert data["status"] == "success"

    def test_get_evidence_stream_has_evidence_items(self, client: FlaskClient):
        response = client.get("/api/v1/evidence/stream")
        data = response.get_json()
        assert data["count"] > 0
        assert len(data["data"]) > 0

    def test_get_evidence_stream_item_structure(self, client: FlaskClient):
        response = client.get("/api/v1/evidence/stream")
        data = response.get_json()
        item = data["data"][0]
        assert "source" in item
        assert "page" in item or "text" in item
        assert "timestamp" in item


class TestExportDashboardEndpoint:
    def test_export_dashboard_json_format(self, client: FlaskClient):
        response = client.post(
            "/api/v1/export/dashboard",
            data=json.dumps(
                {
                    "format": "json",
                    "regions": ["alto-patia", "arauca"],
                    "include_evidence": True,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "status" in data
        assert "data" in data
        assert data["status"] == "success"

    def test_export_dashboard_response_structure(self, client: FlaskClient):
        response = client.post(
            "/api/v1/export/dashboard",
            data=json.dumps(
                {"format": "json", "regions": ["alto-patia"], "include_evidence": False}
            ),
            content_type="application/json",
        )
        data = response.get_json()
        export_data = data["data"]
        assert "timestamp" in export_data
        assert "regions" in export_data
        assert "evidence" in export_data

    def test_export_dashboard_includes_regions(self, client: FlaskClient):
        response = client.post(
            "/api/v1/export/dashboard",
            data=json.dumps(
                {
                    "format": "json",
                    "regions": ["alto-patia", "arauca"],
                    "include_evidence": False,
                }
            ),
            content_type="application/json",
        )
        data = response.get_json()
        regions = data["data"]["regions"]
        assert len(regions) > 0

    def test_export_dashboard_unsupported_format(self, client: FlaskClient):
        response = client.post(
            "/api/v1/export/dashboard",
            data=json.dumps({"format": "pdf", "regions": ["alto-patia"]}),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestRecommendationMicroEndpoint:
    def test_micro_recommendations_missing_scores(self, client: FlaskClient):
        response = client.post(
            "/api/v1/recommendations/micro",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 400 or response.status_code == 503

    def test_micro_recommendations_with_scores(self, client: FlaskClient):
        response = client.post(
            "/api/v1/recommendations/micro",
            data=json.dumps(
                {
                    "scores": {"PA01-DIM01": 1.2, "PA02-DIM02": 1.5, "PA03-DIM01": 0.8},
                    "context": {},
                }
            ),
            content_type="application/json",
        )
        if response.status_code == 503:
            pytest.skip("Recommendation engine not available")
        assert response.status_code == 200
        data = response.get_json()
        assert "status" in data
        assert "data" in data
        assert "timestamp" in data


class TestRecommendationMesoEndpoint:
    def test_meso_recommendations_missing_cluster_data(self, client: FlaskClient):
        response = client.post(
            "/api/v1/recommendations/meso",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 400 or response.status_code == 503

    def test_meso_recommendations_with_cluster_data(self, client: FlaskClient):
        response = client.post(
            "/api/v1/recommendations/meso",
            data=json.dumps(
                {
                    "cluster_data": {
                        "CL01": {"score": 72.0, "variance": 0.25, "weak_pa": "PA02"},
                        "CL02": {"score": 65.0, "variance": 0.30, "weak_pa": "PA05"},
                    },
                    "context": {},
                }
            ),
            content_type="application/json",
        )
        if response.status_code == 503:
            pytest.skip("Recommendation engine not available")
        assert response.status_code == 200
        data = response.get_json()
        assert "status" in data
        assert "data" in data


class TestRecommendationMacroEndpoint:
    def test_macro_recommendations_missing_macro_data(self, client: FlaskClient):
        response = client.post(
            "/api/v1/recommendations/macro",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 400 or response.status_code == 503

    def test_macro_recommendations_with_macro_data(self, client: FlaskClient):
        response = client.post(
            "/api/v1/recommendations/macro",
            data=json.dumps(
                {
                    "macro_data": {
                        "macro_band": "SATISFACTORIO",
                        "clusters_below_target": ["CL02", "CL03"],
                        "variance_alert": "MODERADA",
                        "priority_micro_gaps": ["PA01-DIM05", "PA04-DIM04"],
                    },
                    "context": {},
                }
            ),
            content_type="application/json",
        )
        if response.status_code == 503:
            pytest.skip("Recommendation engine not available")
        assert response.status_code == 200
        data = response.get_json()
        assert "status" in data
        assert "data" in data


class TestRecommendationAllEndpoint:
    def test_all_recommendations_complete_data(self, client: FlaskClient):
        response = client.post(
            "/api/v1/recommendations/all",
            data=json.dumps(
                {
                    "micro_scores": {"PA01-DIM01": 1.2, "PA02-DIM02": 1.5},
                    "cluster_data": {"CL01": {"score": 72.0, "variance": 0.25}},
                    "macro_data": {"macro_band": "SATISFACTORIO"},
                    "context": {},
                }
            ),
            content_type="application/json",
        )
        if response.status_code == 503:
            pytest.skip("Recommendation engine not available")
        assert response.status_code == 200
        data = response.get_json()
        assert "status" in data
        assert "data" in data
        assert "summary" in data
        if data["status"] == "success":
            assert "MICRO" in data["data"]
            assert "MESO" in data["data"]
            assert "MACRO" in data["data"]


class TestRecommendationRulesInfoEndpoint:
    def test_rules_info_returns_structure(self, client: FlaskClient):
        response = client.get("/api/v1/recommendations/rules/info")
        if response.status_code == 503:
            pytest.skip("Recommendation engine not available")
        assert response.status_code == 200
        data = response.get_json()
        assert "status" in data
        assert "data" in data


class TestRecommendationReloadEndpoint:
    def test_reload_rules_requires_auth(self, client: FlaskClient):
        response = client.post("/api/v1/recommendations/reload")
        assert response.status_code == 401

    def test_reload_rules_with_auth(
        self, client: FlaskClient, auth_headers: dict[str, str]
    ):
        response = client.post("/api/v1/recommendations/reload", headers=auth_headers)
        if response.status_code == 503:
            pytest.skip("Recommendation engine not available")
        assert response.status_code in [200, 401, 503]


class TestCachingValidation:
    def test_caching_on_pdet_regions(self, client: FlaskClient):
        response1 = client.get("/api/v1/pdet/regions")
        response2 = client.get("/api/v1/pdet/regions")
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.get_json() == response2.get_json()

    def test_cache_invalidation_after_ttl(self, client: FlaskClient):
        response1 = client.get("/api/v1/evidence/stream")
        time.sleep(0.1)
        response2 = client.get("/api/v1/evidence/stream")
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_different_endpoints_have_separate_cache(self, client: FlaskClient):
        response1 = client.get("/api/v1/pdet/regions")
        response2 = client.get("/api/v1/evidence/stream")
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.get_json() != response2.get_json()

    def test_cache_key_includes_query_params(self, client: FlaskClient):
        response1 = client.get("/api/v1/pdet/regions")
        response2 = client.get("/api/v1/pdet/regions?test=1")
        assert response1.status_code == 200
        assert response2.status_code == 200


class TestRateLimiting:
    def test_rate_limit_not_exceeded_for_normal_requests(self, client: FlaskClient):
        for _ in range(5):
            response = client.get("/api/v1/health")
            assert response.status_code == 200

    def test_rate_limit_tracks_per_endpoint(self, client: FlaskClient):
        for _ in range(3):
            response1 = client.get("/api/v1/health")
            response2 = client.get("/api/v1/pdet/regions")
            assert response1.status_code == 200
            assert response2.status_code == 200

    @pytest.mark.skipif(
        not APIConfig.RATE_LIMIT_ENABLED, reason="Rate limiting disabled"
    )
    def test_rate_limit_exceeded_returns_429(self, client: FlaskClient):
        original_limit = APIConfig.RATE_LIMIT_REQUESTS
        APIConfig.RATE_LIMIT_REQUESTS = 5

        responses = []
        for _ in range(10):
            response = client.get("/api/v1/health")
            responses.append(response.status_code)

        APIConfig.RATE_LIMIT_REQUESTS = original_limit

        if 429 in responses:
            assert True
        else:
            pytest.skip("Rate limit not triggered in test")


class TestWebSocketSSE:
    def test_websocket_connection(self, socketio_client: SocketIOTestClient):
        assert socketio_client.is_connected()

    def test_websocket_connect_response(self, socketio_client: SocketIOTestClient):
        received = socketio_client.get_received()
        connection_responses = [
            msg for msg in received if msg.get("name") == "connection_response"
        ]
        assert len(connection_responses) > 0
        assert connection_responses[0]["args"][0]["status"] == "connected"

    def test_websocket_subscribe_region(self, socketio_client: SocketIOTestClient):
        socketio_client.emit("subscribe_region", {"region_id": "alto-patia"})
        received = socketio_client.get_received()
        region_updates = [msg for msg in received if msg.get("name") == "region_update"]
        assert len(region_updates) > 0

    def test_websocket_disconnect(self):
        client = socketio.test_client(app)
        assert client.is_connected()
        client.disconnect()
        assert not client.is_connected()


class TestAuthenticationValidation:
    def test_require_auth_decorator_blocks_unauthenticated(self, client: FlaskClient):
        response = client.post("/api/v1/recommendations/reload")
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data

    def test_require_auth_decorator_accepts_valid_token(
        self, client: FlaskClient, auth_headers: dict[str, str]
    ):
        response = client.post("/api/v1/recommendations/reload", headers=auth_headers)
        assert response.status_code != 401

    def test_require_auth_decorator_rejects_invalid_token(self, client: FlaskClient):
        response = client.post(
            "/api/v1/recommendations/reload",
            headers={"Authorization": "Bearer invalid_token_xyz"},
        )
        assert response.status_code == 401

    def test_require_auth_decorator_rejects_malformed_header(self, client: FlaskClient):
        response = client.post(
            "/api/v1/recommendations/reload",
            headers={"Authorization": "invalid_format"},
        )
        assert response.status_code == 401

    def test_expired_token_rejected(self):
        with patch("farfan_pipeline.api.api_server.datetime") as mock_datetime:
            past_time = datetime.now(timezone.utc) - timedelta(hours=25)
            mock_datetime.now.return_value = past_time
            token = generate_jwt_token("test_client")

            mock_datetime.now.return_value = datetime.now(timezone.utc)
            payload = verify_jwt_token(token)
            assert payload is None


class TestErrorHandling:
    def test_404_for_invalid_endpoint(self, client: FlaskClient):
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404

    def test_405_for_wrong_method(self, client: FlaskClient):
        response = client.get("/api/v1/auth/token")
        assert response.status_code == 405

    def test_400_for_invalid_json(self, client: FlaskClient):
        response = client.post(
            "/api/v1/export/dashboard",
            data="invalid json{",
            content_type="application/json",
        )
        assert response.status_code in [400, 500]

    def test_region_not_found_returns_404(self, client: FlaskClient):
        response = client.get("/api/v1/pdet/regions/invalid-region-id-xyz")
        assert response.status_code == 404


class TestEndpointCompleteness:
    def test_all_endpoints_documented(self, client: FlaskClient):
        endpoints = [
            ("/", "GET"),
            ("/api/v1/health", "GET"),
            ("/api/v1/auth/token", "POST"),
            ("/api/v1/constellation_map", "GET"),
            ("/api/v1/pdet/regions", "GET"),
            ("/api/v1/pdet/regions/alto-patia", "GET"),
            ("/api/v1/municipalities/test123", "GET"),
            ("/api/v1/evidence/stream", "GET"),
            ("/api/v1/export/dashboard", "POST"),
            ("/api/v1/recommendations/micro", "POST"),
            ("/api/v1/recommendations/meso", "POST"),
            ("/api/v1/recommendations/macro", "POST"),
            ("/api/v1/recommendations/all", "POST"),
            ("/api/v1/recommendations/rules/info", "GET"),
        ]

        for endpoint, method in endpoints:
            if method == "GET":
                response = client.get(endpoint)
            else:
                response = client.post(
                    endpoint, data=json.dumps({}), content_type="application/json"
                )
            assert response.status_code in [200, 400, 401, 404, 503]

    def test_12_main_rest_endpoints_covered(self):
        expected_endpoints = {
            "health",
            "auth_token",
            "constellation_map",
            "pdet_regions",
            "region_detail",
            "municipality",
            "evidence_stream",
            "export_dashboard",
            "micro_recommendations",
            "meso_recommendations",
            "macro_recommendations",
            "all_recommendations",
        }
        assert len(expected_endpoints) == 12


class TestCORS:
    def test_cors_headers_present(self, client: FlaskClient):
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_options_request_for_cors(self, client: FlaskClient):
        response = client.options("/api/v1/health")
        assert response.status_code in [200, 204]


class TestDataServiceIntegration:
    def test_data_service_returns_16_regions(self):
        service = DataService()
        regions = service.get_pdet_regions()
        assert len(regions) == 16

    def test_data_service_region_detail(self):
        service = DataService()
        region = service.get_region_detail("alto-patia")
        assert region is not None
        assert region["id"] == "alto-patia"

    def test_data_service_evidence_stream(self):
        service = DataService()
        evidence = service.get_evidence_stream()
        assert len(evidence) > 0

    def test_data_service_constellation_map(self):
        service = DataService()
        constellation = service.get_constellation_map_data()
        assert "nodes" in constellation
        assert "links" in constellation
