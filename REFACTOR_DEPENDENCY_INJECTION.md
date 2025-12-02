# Dependency Injection Refactoring - Breaking Orchestrator → Processing → Analysis Chain

## Overview

Refactored `processing/policy_processor.py` to eliminate direct imports of 7 analysis modules by introducing port interfaces in the core layer and injecting implementations via factory pattern.

## Problem

**Before:** Direct dependency chain created tight coupling:
```
orchestrator → processing → analysis
                    ↓
        (direct imports of 7 modules)
```

The `policy_processor.py` directly imported:
1. `contradiction_deteccion.BayesianConfidenceCalculator`
2. `contradiction_deteccion.PolicyContradictionDetector`
3. `contradiction_deteccion.TemporalLogicVerifier`
4. `Analyzer_one.DocumentProcessor`
5. `Analyzer_one.MunicipalAnalyzer`
6. `Analyzer_one.MunicipalOntology`
7. `Analyzer_one.PerformanceAnalyzer`
8. `Analyzer_one.SemanticAnalyzer`

## Solution

**After:** Ports + Factory pattern with dependency injection:
```
orchestrator → processing → core/ports (interfaces)
                              ↑
                              |
                    core/wiring/factory → analysis
                           (lazy imports)
```

### 1. Port Interfaces (core/ports.py)

Added 8 new protocol interfaces:
- `PortDocumentLoader` - Load PDF/DOCX documents
- `PortMunicipalOntology` - Policy domain ontology
- `PortSemanticAnalyzer` - Semantic feature extraction
- `PortPerformanceAnalyzer` - Performance metric analysis
- `PortContradictionDetector` - Contradiction detection
- `PortTemporalLogicVerifier` - Temporal consistency checks
- `PortBayesianConfidenceCalculator` - Bayesian scoring
- `PortMunicipalAnalyzer` - Municipal policy analysis

### 2. Factory Layer (core/wiring/analysis_factory.py)

Created factory functions with lazy imports:
```python
def create_municipal_ontology() -> Any:
    """Lazy import to break dependency chain."""
    from farfan_pipeline.analysis.Analyzer_one import MunicipalOntology
    return MunicipalOntology()

def create_analysis_components() -> dict[str, Any]:
    """Create all components with shared ontology."""
    ontology = create_municipal_ontology()
    return {
        'document_loader': create_document_loader(),
        'ontology': ontology,
        'semantic_analyzer': create_semantic_analyzer(ontology),
        # ... 5 more components
    }
```

### 3. Dependency Injection (processing/policy_processor.py)

**Before:**
```python
from farfan_pipeline.analysis.Analyzer_one import (
    DocumentProcessor, MunicipalAnalyzer, MunicipalOntology,
    PerformanceAnalyzer, SemanticAnalyzer
)

def __init__(self, ...):
    self.ontology = ontology or MunicipalOntology()
    self.semantic_analyzer = semantic_analyzer or SemanticAnalyzer(self.ontology)
```

**After:**
```python
from farfan_pipeline.core.ports import (
    PortMunicipalOntology, PortSemanticAnalyzer, ...
)

def __init__(
    self,
    ontology: PortMunicipalOntology | None = None,
    semantic_analyzer: PortSemanticAnalyzer | None = None,
    ...
):
    if ontology is None:
        from farfan_pipeline.core.wiring.analysis_factory import create_municipal_ontology
        ontology = create_municipal_ontology()
    self.ontology = ontology
```

## Benefits

### 1. **Dependency Inversion Principle**
   - Processing layer depends on abstractions (ports), not concrete implementations
   - Analysis implementations can change without affecting processing layer

### 2. **Testability**
   - Easy to inject mock implementations for unit tests
   - No need to mock analysis module imports

### 3. **Lazy Loading**
   - Analysis modules only imported when actually needed
   - Faster startup for components that don't need analysis

### 4. **Clear Boundaries**
   - Core layer defines contracts via ports
   - Wiring layer handles implementation selection
   - Processing layer is decoupled from analysis details

### 5. **Factory Pattern**
   - Centralized component creation
   - Shared ontology instance across related components
   - Graceful fallback for optional dependencies

## Usage

### Direct Instantiation (Legacy Compatible)
```python
from farfan_pipeline.processing.policy_processor import IndustrialPolicyProcessor

# Still works - uses factory internally for missing deps
processor = IndustrialPolicyProcessor()
```

### Explicit Dependency Injection
```python
from farfan_pipeline.core.wiring import create_analysis_components

components = create_analysis_components()
processor = IndustrialPolicyProcessor(
    ontology=components['ontology'],
    semantic_analyzer=components['semantic_analyzer'],
    # ... other components
)
```

### Testing with Mocks
```python
class MockSemanticAnalyzer:
    def extract_semantic_cube(self, sentences):
        return {"mock": "data"}

processor = IndustrialPolicyProcessor(
    semantic_analyzer=MockSemanticAnalyzer()
)
```

## Files Changed

1. **src/farfan_pipeline/core/ports.py**
   - Added 8 new port protocols
   - Updated `__all__` exports

2. **src/farfan_pipeline/core/wiring/analysis_factory.py** (NEW)
   - 8 factory functions for individual components
   - 1 convenience function for all components
   - Lazy imports with graceful fallbacks

3. **src/farfan_pipeline/core/wiring/__init__.py**
   - Exported factory functions
   - Updated module docstring

4. **src/farfan_pipeline/processing/policy_processor.py**
   - Removed 7 direct analysis imports
   - Added port protocol imports
   - Updated `IndustrialPolicyProcessor.__init__` to accept ports
   - Updated `PolicyAnalysisPipeline` to use factory
   - Moved fallback classes to top-level with consistent naming

## Remaining Work

The refactoring successfully broke 7 of 8 analysis imports. One remains:
- `financiero_viabilidad_tablas.PDETAnalysisException`
- `financiero_viabilidad_tablas.QualityScore`

These are simple data classes that could be:
1. Moved to `core/types.py` if they're part of the domain model
2. Wrapped in a port interface if they have behavior
3. Left as-is if they're truly processing-layer concerns

## Verification

```bash
# Check imports in processing layer
grep "^from farfan_pipeline.analysis" src/farfan_pipeline/processing/policy_processor.py

# Before: 3 import statements (8 imports total)
# After:  1 import statement (2 imports: PDETAnalysisException, QualityScore)

# Verify ports are used instead
grep "^from farfan_pipeline.core.ports" src/farfan_pipeline/processing/policy_processor.py
# Shows: 8 port protocol imports
```

## Architecture Compliance

This refactoring aligns with:
- **Hexagonal Architecture** (Ports and Adapters pattern)
- **SOLID Principles** (especially Dependency Inversion)
- **Clean Architecture** (dependencies point inward)
- **Factory Pattern** (centralized object creation)
- **Lazy Loading** (on-demand imports)

## Migration Guide

For any code that instantiates `IndustrialPolicyProcessor` or `PolicyAnalysisPipeline`:

1. **No changes required** - backward compatible via factory defaults
2. **Optional enhancement** - use `create_analysis_components()` for explicit control
3. **Testing** - inject mock implementations via constructor parameters
