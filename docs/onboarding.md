# Onboarding Praetor (Bitácora Digital para chat LLM)

Objetivo: registrar cada conversación del chat en un archivo diario con hash encadenado y sellarlo al final del turno para custodia física.

## 1) Preparar el entorno (sin internet)
```bash
python -m venv .venv
source .venv/bin/activate
pip install --no-cache-dir -r requirements.offline.txt
```

## 2) Variables mínimas
```bash
export PRAETOR_BITACORA_DIR=exports/bitacora
export PRAETOR_AUDIT_LOG_PATH=data/audit.log
```

## 3) Encender Praetor
```bash
PYTHONPATH=src uvicorn praetor_gateway.main:app --host 127.0.0.1 --port 8000
```
Déjalo corriendo; solo registra, no bloquea.

## 4) Registrar un mensaje de chat
```bash
curl -X POST http://127.0.0.1:8000/v1/authorize \
  -H 'Content-Type: application/json' \
  -d '{"action":"chat/output","classification":"PUBLICA","agent_id":"usuario1","message":"texto enviado","response":"texto devuelto"}'
```
Cada llamada se guarda en `exports/bitacora/<hostname>/log_YYYYMMDD.txt` con hash encadenado.

## 5) Sellar al final del turno
```bash
./scripts/cerrar_turno.sh
```
Genera `log_YYYYMMDD.txt.sha256`. Copia ambos archivos (log + sha256) al USB y entrégalos en el cambio de guardia.

Listo: tienes un libro de bitácora digital inmutable, sin fricción para el chat ni dependencias externas.
