# IMPORT_AUDIT.md

## ESTADO ACTUAL DEL SISTEMA DE IMPORTS

### Resumen Ejecutivo

- **Total de archivos Python analizados**: 307
- **Archivos con imports relativos**: 47
- **Archivos con manipulación de sys.path**: 5
- **Archivos con llamadas a os.chdir**: 0

### Estructura Actual del Repositorio

El repositorio contiene una estructura **NO ESTÁNDAR**:

```
.
├── farfan_core/
│   └── farfan_core/  # <-- Nested package (NO PEP 420 compliant)
│       ├── __init__.py
│       ├── core/
│       ├── analysis/
│       ├── processing/
│       └── ...
├── scripts/
├── tests/
├── tools/
└── pyproject.toml
```

**PROBLEMA CRÍTICO**: La estructura actual tiene el paquete duplicado (`farfan_core/farfan_core/`) y viola PEP 420.

### Archivos con Manipulación de sys.path

- `./debug_walk.py` - Líneas 6-7
- `./scripts/dev/analyze_circular_imports.py` - Línea 413
- `./scripts/validators/validate_calibration_system.py` - Línea 13
- `./farfan_core/farfan_core/devtools/ensure_install.py` - Líneas 30, 37
- `./farfan_core/farfan_core/entrypoint/main.py` - Línea 49 (debug print)

### Namespace Raíz Inferido

**Paquete Canónico Propuesto**: `farfan_pipeline`

**Justificación**:
- El nombre actual `farfan_core` es ambiguo y crea confusión con la estructura anidada
- `farfan_pipeline` refleja mejor el propósito del sistema (mechanistic policy pipeline)
- Es más distintivo y evita conflictos con el módulo `core` interno

### Estructura Propuesta (PEP 420 Compliant)

```
.
├── src/
│   └── farfan_pipeline/  # <-- Canonical package name
│       ├── __init__.py
│       ├── core/
│       ├── analysis/
│       ├── processing/
│       ├── infrastructure/
│       ├── api/
│       ├── contracts/
│       ├── utils/
│       └── entrypoint/
├── tests/
├── scripts/
├── tools/
├── pyproject.toml
└── README.md
```

### Anomalías Detectadas

1. **Estructura anidada duplicada**: `farfan_core/farfan_core/` debe colapsarse a `src/farfan_pipeline/`
2. **Imports relativos**: 345 imports relativos deben convertirse a absolutos
3. **Manipulación de sys.path**: 5 archivos manipulan sys.path, debe eliminarse
4. **pyproject.toml incorrecto**: `where = ["farfan_core"]` debe ser `where = ["src"]`
5. **pythonpath en pytest**: Configuración incorrecta debe eliminarse con src-layout

---
**Fecha**: 2025-12-01  
**Generado por**: Agente de Ingeniería Autónoma
