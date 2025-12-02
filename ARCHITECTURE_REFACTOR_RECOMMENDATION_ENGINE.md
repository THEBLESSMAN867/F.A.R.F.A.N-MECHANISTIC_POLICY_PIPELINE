# Recommendation Engine Architecture Refactoring

## Overview

This refactoring introduces the **Ports and Adapters (Hexagonal Architecture)** pattern for the recommendation engine, decoupling the orchestrator from the concrete `RecommendationEngine` implementation.

## Changes Made

### 1. New Port Interface: `core/analysis_port.py`

Created `RecommendationEnginePort` protocol that defines the abstract interface for recommendation generation:

```python
class RecommendationEnginePort(Protocol):
    def generate_all_recommendations(...) -> dict[str, Any]: ...
    def generate_micro_recommendations(...) -> Any: ...
    def generate_meso_recommendations(...) -> Any: ...
    def generate_macro_recommendations(...) -> Any: ...
    def reload_rules() -> None: ...
```

**Benefits:**
- Clear contract for recommendation engine capabilities
- Orchestrator depends on abstraction, not concrete implementation
- Easier to test with mock implementations
- Future alternative implementations can be swapped without changing orchestrator

### 2. New Adapter: `infrastructure/recommendation_engine_adapter.py`

Created `RecommendationEngineAdapter` that implements the port using the concrete `RecommendationEngine` from `analysis/recommendation_engine.py`:

```python
class RecommendationEngineAdapter:
    def __init__(self, rules_path, schema_path, questionnaire_provider, orchestrator): ...
    def generate_all_recommendations(...): ...
    # ... implements all port methods
```

Factory function for easy instantiation:

```python
def create_recommendation_engine_adapter(...) -> RecommendationEngineAdapter: ...
```

**Benefits:**
- Infrastructure layer handles concrete implementation details
- Isolates I/O operations (file loading) from core logic
- Handles circular dependency between orchestrator and engine via `set_orchestrator()`

### 3. Updated Orchestrator: `core/orchestrator/core.py`

**Before:**
```python
from ...analysis.recommendation_engine import RecommendationEngine

class Orchestrator:
    def __init__(self, ...):
        self.recommendation_engine = RecommendationEngine(
            rules_path=RULES_DIR / "...",
            schema_path=RULES_DIR / "...",
            ...
        )
```

**After:**
```python
from ..analysis_port import RecommendationEnginePort

class Orchestrator:
    def __init__(self, ..., recommendation_engine_port: RecommendationEnginePort | None = None):
        self.recommendation_engine = recommendation_engine_port
```

**Benefits:**
- Orchestrator no longer instantiates recommendation engine directly
- Dependency injection enables testing with mock ports
- No direct import of analysis module (follows layered architecture)

### 4. Updated Factory: `core/orchestrator/factory.py`

Factory now creates and injects the adapter:

```python
def create_orchestrator() -> "Orchestrator":
    recommendation_engine_port = create_recommendation_engine_adapter(
        rules_path=RULES_DIR / "recommendation_rules_enhanced.json",
        schema_path=RULES_DIR / "recommendation_rules_enhanced.schema.json",
        questionnaire_provider=questionnaire_provider,
        orchestrator=None  # Set after orchestrator creation
    )
    
    orchestrator = Orchestrator(
        ...,
        recommendation_engine_port=recommendation_engine_port,
    )
    
    # Handle circular dependency
    if recommendation_engine_port is not None:
        recommendation_engine_port.set_orchestrator(orchestrator)
    
    return orchestrator
```

**Benefits:**
- Single responsibility: factory handles wiring
- Circular dependency handled cleanly
- Easy to override adapter for testing

### 5. Updated Exports: `core/ports.py` and `infrastructure/__init__.py`

Added proper exports for the new modules:

```python
# core/ports.py
from .analysis_port import RecommendationEnginePort
__all__ = [..., 'RecommendationEnginePort']

# infrastructure/__init__.py
from .recommendation_engine_adapter import (
    RecommendationEngineAdapter,
    create_recommendation_engine_adapter,
)
__all__ = [...]
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Core Layer                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Orchestrator (core/orchestrator/core.py)        │  │
│  │  - depends on RecommendationEnginePort (abstract)│  │
│  │  - no knowledge of concrete implementation       │  │
│  └───────────────────┬──────────────────────────────┘  │
│                      │ depends on                       │
│  ┌───────────────────▼──────────────────────────────┐  │
│  │  RecommendationEnginePort (core/analysis_port.py)│  │
│  │  - Protocol (abstract interface)                 │  │
│  │  - Defines contract for recommendation engine    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                             ▲
                             │ implements
┌─────────────────────────────────────────────────────────┐
│               Infrastructure Layer                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  RecommendationEngineAdapter                     │  │
│  │  (infrastructure/recommendation_engine_adapter.py)│  │
│  │  - Implements RecommendationEnginePort           │  │
│  │  - Wraps concrete RecommendationEngine           │  │
│  └───────────────────┬──────────────────────────────┘  │
│                      │ uses                             │
│  ┌───────────────────▼──────────────────────────────┐  │
│  │  RecommendationEngine                            │  │
│  │  (analysis/recommendation_engine.py)             │  │
│  │  - Concrete implementation                       │  │
│  │  - Loads rules, validates, generates recs        │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Testing Strategy

### Unit Testing the Adapter

```python
def test_adapter_implements_port():
    adapter = RecommendationEngineAdapter(...)
    assert isinstance(adapter, RecommendationEnginePort)

def test_adapter_delegates_to_engine():
    adapter = RecommendationEngineAdapter(...)
    result = adapter.generate_all_recommendations(...)
    # Assert result structure
```

### Testing Orchestrator with Mock Port

```python
from unittest.mock import Mock

def test_orchestrator_with_mock_engine():
    mock_engine = Mock(spec=RecommendationEnginePort)
    mock_engine.generate_all_recommendations.return_value = {...}
    
    orchestrator = Orchestrator(
        ...,
        recommendation_engine_port=mock_engine
    )
    
    # Test orchestrator behavior without real engine
```

## Migration Guide

### For Code Using `create_orchestrator()`

No changes needed! The factory handles the new dependency injection transparently.

### For Code Directly Instantiating Orchestrator

**Before:**
```python
orchestrator = Orchestrator(method_executor, questionnaire, config)
```

**After:**
```python
from farfan_pipeline.infrastructure import create_recommendation_engine_adapter

recommendation_engine = create_recommendation_engine_adapter(...)
orchestrator = Orchestrator(
    method_executor,
    questionnaire,
    config,
    recommendation_engine_port=recommendation_engine
)
recommendation_engine.set_orchestrator(orchestrator)
```

### For Testing

**Before:** Had to mock internals of orchestrator

**After:** Can inject mock port:
```python
mock_engine = Mock(spec=RecommendationEnginePort)
orchestrator = Orchestrator(..., recommendation_engine_port=mock_engine)
```

## Benefits Summary

1. **Separation of Concerns**: Orchestrator focuses on orchestration, not recommendation implementation
2. **Dependency Inversion**: Core depends on abstractions, infrastructure implements them
3. **Testability**: Easy to test with mock implementations
4. **Flexibility**: Can swap implementations without changing orchestrator
5. **Clean Architecture**: Follows hexagonal/ports-and-adapters pattern
6. **Type Safety**: Protocol ensures contract compliance
7. **Maintainability**: Clear boundaries between layers

## Files Modified

- ✨ NEW: `src/farfan_pipeline/core/analysis_port.py`
- ✨ NEW: `src/farfan_pipeline/infrastructure/recommendation_engine_adapter.py`
- 🔧 MODIFIED: `src/farfan_pipeline/core/orchestrator/core.py`
- 🔧 MODIFIED: `src/farfan_pipeline/core/orchestrator/factory.py`
- 🔧 MODIFIED: `src/farfan_pipeline/core/ports.py`
- 🔧 MODIFIED: `src/farfan_pipeline/infrastructure/__init__.py`

## Backward Compatibility

✅ **Fully backward compatible**

- Existing code using `create_orchestrator()` works without changes
- `RecommendationEngine` still exists and functions as before
- New parameter is optional (`recommendation_engine_port: ... | None = None`)
- If port is not provided, orchestrator logs warning and continues
