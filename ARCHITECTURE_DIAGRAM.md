# Architecture Diagram - Dependency Injection Refactoring

## Before Refactoring: Direct Dependencies

```
┌─────────────────────┐
│   orchestrator/     │
│   orchestrator.py   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────────┐
│         processing/                         │
│      policy_processor.py                    │
│                                             │
│  Direct Imports:                            │
│  • BayesianConfidenceCalculator            │
│  • PolicyContradictionDetector             │
│  • TemporalLogicVerifier                   │
│  • DocumentProcessor                        │
│  • MunicipalAnalyzer                        │
│  • MunicipalOntology                        │
│  • PerformanceAnalyzer                      │
│  • SemanticAnalyzer                         │
└──────────┬──────────────────────────────────┘
           │
           │ (8 direct imports)
           │
           ▼
┌─────────────────────────────────────────────┐
│            analysis/                        │
│  ┌────────────────────────────────┐        │
│  │  contradiction_deteccion.py    │        │
│  │  • BayesianConfidenceCalculator│        │
│  │  • PolicyContradictionDetector │        │
│  │  • TemporalLogicVerifier       │        │
│  └────────────────────────────────┘        │
│                                             │
│  ┌────────────────────────────────┐        │
│  │      Analyzer_one.py           │        │
│  │  • DocumentProcessor           │        │
│  │  • MunicipalAnalyzer           │        │
│  │  • MunicipalOntology           │        │
│  │  • PerformanceAnalyzer         │        │
│  │  • SemanticAnalyzer            │        │
│  └────────────────────────────────┘        │
└─────────────────────────────────────────────┘

Problem: Tight coupling, hard to test, circular dependencies
```

## After Refactoring: Ports + Factory Pattern

```
┌─────────────────────┐
│   orchestrator/     │
│   orchestrator.py   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────────┐
│         processing/                         │
│      policy_processor.py                    │
│                                             │
│  Constructor Parameters (Ports):            │
│  • PortBayesianConfidenceCalculator        │
│  • PortContradictionDetector               │
│  • PortTemporalLogicVerifier               │
│  • PortDocumentLoader                       │
│  • PortMunicipalAnalyzer                    │
│  • PortMunicipalOntology                    │
│  • PortPerformanceAnalyzer                  │
│  • PortSemanticAnalyzer                     │
└──────────┬──────────────────────────────────┘
           │
           │ (depends on interfaces only)
           │
           ▼
┌─────────────────────────────────────────────┐
│              core/                          │
│            ports.py                         │
│                                             │
│  Protocol Interfaces (no dependencies):     │
│  • PortBayesianConfidenceCalculator        │
│  • PortContradictionDetector               │
│  • PortTemporalLogicVerifier               │
│  • PortDocumentLoader                       │
│  • PortMunicipalAnalyzer                    │
│  • PortMunicipalOntology                    │
│  • PortPerformanceAnalyzer                  │
│  • PortSemanticAnalyzer                     │
└─────────────────────────────────────────────┘
           ▲
           │ (defines contracts)
           │
┌──────────┴──────────────────────────────────┐
│         core/wiring/                        │
│      analysis_factory.py                    │
│                                             │
│  Factory Functions (lazy imports):          │
│  • create_bayesian_confidence_calculator() │
│  • create_contradiction_detector()         │
│  • create_temporal_logic_verifier()        │
│  • create_document_loader()                │
│  • create_municipal_analyzer()             │
│  • create_municipal_ontology()             │
│  • create_performance_analyzer()           │
│  • create_semantic_analyzer()              │
│  • create_analysis_components() ────────┐  │
└──────────┬──────────────────────────────┼───┘
           │                              │
           │ (imports on-demand)          │
           │                              │
           ▼                              │
┌─────────────────────────────────────────┼───┐
│            analysis/                    │   │
│  ┌────────────────────────────────┐    │   │
│  │  contradiction_deteccion.py    │◄───┘   │
│  │  • BayesianConfidenceCalculator│        │
│  │  • PolicyContradictionDetector │        │
│  │  • TemporalLogicVerifier       │        │
│  └────────────────────────────────┘        │
│                                             │
│  ┌────────────────────────────────┐        │
│  │      Analyzer_one.py           │◄───────┘
│  │  • DocumentProcessor           │
│  │  • MunicipalAnalyzer           │
│  │  • MunicipalOntology           │
│  │  • PerformanceAnalyzer         │
│  │  • SemanticAnalyzer            │
│  └────────────────────────────────┘
└─────────────────────────────────────────────┘

Benefits:
✓ Loose coupling via interfaces
✓ Easy to test with mocks
✓ Lazy loading (imports on-demand)
✓ Dependency Inversion Principle
✓ Factory Pattern for object creation
```

## Dependency Flow

### Before
```
orchestrator → processing → analysis
     (tight coupling)
```

### After
```
orchestrator → processing → core/ports
                   ↑            ↓
                   └──── core/wiring/factory → analysis
                        (dependency injection)
```

## Key Architectural Patterns

1. **Hexagonal Architecture (Ports and Adapters)**
   - `core/ports.py` = Ports (interfaces)
   - `analysis/*` = Adapters (implementations)

2. **Dependency Inversion Principle**
   - High-level (processing) depends on abstractions (ports)
   - Low-level (analysis) implements abstractions

3. **Factory Pattern**
   - `analysis_factory.py` creates objects
   - Centralizes dependencies
   - Enables lazy loading

4. **Dependency Injection**
   - Constructor injection via parameters
   - Defaults use factory for backward compatibility
   - Easy to override for testing

## Testing Strategy

### Unit Tests (with mocks)
```python
class MockSemanticAnalyzer:
    def extract_semantic_cube(self, sentences):
        return {"mock": "data"}

processor = IndustrialPolicyProcessor(
    semantic_analyzer=MockSemanticAnalyzer()
)
```

### Integration Tests (with real implementations)
```python
from farfan_pipeline.core.wiring import create_analysis_components

components = create_analysis_components()
processor = IndustrialPolicyProcessor(**components)
```

### Backward Compatibility
```python
# Still works - uses factory internally
processor = IndustrialPolicyProcessor()
```
