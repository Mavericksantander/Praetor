# Praetor Gateway

Gateway de gobernanza y auditoría air‑gapped para Canopy en despliegues soberanos.

## Requisitos
- Python 3.11+
- pip o pipx

## Instalación rápida
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.offline.txt
```

## Ejecución (dev)
```bash
export PRAETOR_BITACORA_DIR=exports/bitacora
export PRAETOR_AUDIT_LOG_PATH=data/audit.log
export PRAETOR_REPORT_DIR=exports/reports
uvicorn src.praetor_gateway.main:app --reload
```

## Tests
```bash
pytest
```

## Estructura
- `src/praetor_gateway/`: aplicación FastAPI y lógica de auditoría.
- `scripts/`: utilidades operativas.
- `exports/`, `data/`: carpetas de salida (ignoradas en git).

