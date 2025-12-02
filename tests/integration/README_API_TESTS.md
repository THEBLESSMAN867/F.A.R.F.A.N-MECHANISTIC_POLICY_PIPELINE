# API Integration Test Suite

## Overview

Comprehensive integration test suite for the FARFAN API server (`api_server.py`) covering all 12 REST endpoints plus WebSocket SSE functionality, authentication, rate limiting, and caching validation.

## Test Coverage

### Core Endpoints (12)

1. **Health Endpoint** (`/api/v1/health`)
   - Status check
   - Response structure validation
   - Timestamp format verification

2. **Authentication Endpoint** (`/api/v1/auth/token`)
   - Missing credentials handling
   - Token generation
   - JWT validation
   - Token expiration

3. **PDET Regions Endpoint** (`/api/v1/pdet/regions`)
   - List all 16 PDET regions
   - Response structure validation
   - Data integrity checks

4. **PDET Region Detail Endpoint** (`/api/v1/pdet/regions/<id>`)
   - Individual region details
   - 404 handling for invalid regions
   - Detailed analysis structure
   - Question matrix (44 questions)

5. **Constellation Map Endpoint** (`/api/v1/constellation_map`)
   - Node and link structure
   - Visualization data integrity

6. **Municipalities Endpoint** (`/api/v1/municipalities/<id>`)
   - Municipality analysis
   - Radar chart data
   - Cluster breakdown
   - 44-question matrix

7. **Evidence Stream Endpoint** (`/api/v1/evidence/stream`)
   - Real-time evidence ticker
   - Item structure validation
   - Count verification

8. **Export Dashboard Endpoint** (`/api/v1/export/dashboard`)
   - JSON export format
   - Region data inclusion
   - Evidence stream inclusion
   - Unsupported format handling

9. **Recommendation MICRO Endpoint** (`/api/v1/recommendations/micro`)
   - Score-based micro recommendations
   - Missing data validation
   - Response structure

10. **Recommendation MESO Endpoint** (`/api/v1/recommendations/meso`)
    - Cluster-based meso recommendations
    - Variance analysis
    - Context handling

11. **Recommendation MACRO Endpoint** (`/api/v1/recommendations/macro`)
    - Strategic macro recommendations
    - Macro band classification
    - Priority gap identification

12. **Recommendation All Endpoint** (`/api/v1/recommendations/all`)
    - Combined recommendations at all levels
    - Summary statistics
    - Complete context integration

### Additional Endpoints

13. **Recommendation Rules Info** (`/api/v1/recommendations/rules/info`)
    - Rules metadata
    - Version information
    - Rule count by level

14. **Recommendation Reload** (`/api/v1/recommendations/reload`)
    - Auth-protected endpoint
    - Rules hot-reload

## Advanced Feature Tests

### Caching Validation
- Cache hit/miss behavior
- TTL validation
- Cache key uniqueness
- Query parameter handling

### Rate Limiting
- Request counting
- Per-endpoint tracking
- 429 status code on limit exceeded
- Window-based rate limiting

### WebSocket SSE
- Connection establishment
- Connection response validation
- Region subscription
- Real-time updates
- Disconnect handling

### Authentication
- JWT token validation
- Authorization header parsing
- Invalid token rejection
- Expired token handling
- Malformed header detection

### Error Handling
- 404 for invalid endpoints
- 405 for wrong HTTP methods
- 400 for invalid JSON
- Region not found scenarios

### CORS
- CORS header presence
- OPTIONS request handling

## Test Structure

```
tests/integration/test_api_integration.py
├── Fixtures (5)
│   ├── client: Flask test client
│   ├── socketio_client: WebSocket test client
│   ├── auth_token: JWT token generator
│   ├── auth_headers: Auth headers dict
│   └── clear_cache_and_rate_limits: Auto-cleanup
│
└── Test Classes (22)
    ├── TestHealthEndpoint (3 tests)
    ├── TestAuthEndpoint (6 tests)
    ├── TestPDETRegionsEndpoint (6 tests)
    ├── TestPDETRegionDetailEndpoint (7 tests)
    ├── TestConstellationMapEndpoint (3 tests)
    ├── TestMunicipalitiesEndpoint (6 tests)
    ├── TestEvidenceStreamEndpoint (4 tests)
    ├── TestExportDashboardEndpoint (4 tests)
    ├── TestRecommendationMicroEndpoint (2 tests)
    ├── TestRecommendationMesoEndpoint (2 tests)
    ├── TestRecommendationMacroEndpoint (2 tests)
    ├── TestRecommendationAllEndpoint (1 test)
    ├── TestRecommendationRulesInfoEndpoint (1 test)
    ├── TestRecommendationReloadEndpoint (2 tests)
    ├── TestCachingValidation (4 tests)
    ├── TestRateLimiting (3 tests)
    ├── TestWebSocketSSE (4 tests)
    ├── TestAuthenticationValidation (5 tests)
    ├── TestErrorHandling (4 tests)
    ├── TestEndpointCompleteness (2 tests)
    ├── TestCORS (2 tests)
    └── TestDataServiceIntegration (4 tests)
```

**Total: 77 test methods**

## Running the Tests

### Run all API integration tests
```bash
python -m pytest tests/integration/test_api_integration.py -v
```

### Run specific test class
```bash
python -m pytest tests/integration/test_api_integration.py::TestHealthEndpoint -v
```

### Run with coverage
```bash
python -m pytest tests/integration/test_api_integration.py -v --cov=farfan_core.farfan_core.api --cov-report=term-missing
```

### Run specific test method
```bash
python -m pytest tests/integration/test_api_integration.py::TestAuthEndpoint::test_auth_token_successful_generation -v
```

## Dependencies

- pytest >= 7.4.3
- pytest-cov >= 4.1.0
- flask >= 2.3.2
- flask-socketio >= 5.3.6
- flask-cors >= 6.0.0

## Key Features

### 1. Automatic Cleanup
The `clear_cache_and_rate_limits` fixture automatically cleans up cache and rate limit counters before and after each test to ensure test isolation.

### 2. Authentication Handling
The `auth_token` and `auth_headers` fixtures provide easy access to valid JWT tokens for testing authenticated endpoints.

### 3. Conditional Skipping
Tests gracefully skip when the recommendation engine is unavailable (503 status), allowing tests to run even in incomplete environments.

### 4. Comprehensive Validation
Tests validate:
- HTTP status codes
- Response structure
- Data types
- Business logic
- Error scenarios
- Edge cases

## Endpoints Summary

| Endpoint | Method | Auth Required | Cache TTL | Tests |
|----------|--------|---------------|-----------|-------|
| `/api/v1/health` | GET | No | None | 3 |
| `/api/v1/auth/token` | POST | No | None | 6 |
| `/api/v1/constellation_map` | GET | No | 300s | 3 |
| `/api/v1/pdet/regions` | GET | No | 300s | 6 |
| `/api/v1/pdet/regions/<id>` | GET | No | 300s | 7 |
| `/api/v1/municipalities/<id>` | GET | No | 300s | 6 |
| `/api/v1/evidence/stream` | GET | No | 60s | 4 |
| `/api/v1/export/dashboard` | POST | No | None | 4 |
| `/api/v1/recommendations/micro` | POST | No | None | 2 |
| `/api/v1/recommendations/meso` | POST | No | None | 2 |
| `/api/v1/recommendations/macro` | POST | No | None | 2 |
| `/api/v1/recommendations/all` | POST | No | None | 1 |
| `/api/v1/recommendations/rules/info` | GET | No | 600s | 1 |
| `/api/v1/recommendations/reload` | POST | **Yes** | None | 2 |

## Notes

- The recommendation engine endpoints (micro, meso, macro, all) may return 503 if the engine is not initialized
- Rate limiting tests are skipped if `RATE_LIMIT_ENABLED=false`
- WebSocket tests use the `flask_socketio.test_client()` for simulating real-time connections
- All tests use the Flask test client which provides request isolation and doesn't require running the server

## Maintenance

When adding new endpoints to `api_server.py`:
1. Add a new test class following the naming convention `Test<EndpointName>Endpoint`
2. Add tests for success cases, error cases, and edge cases
3. Update this README with the new endpoint information
4. Ensure cache and rate limiting behavior is tested if applicable