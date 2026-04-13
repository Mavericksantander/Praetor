# Onboarding Praetor (Bitácora Digital para chat LLM)

Objetivo: registrar cada consulta al LLM en un archivo diario con hash encadenado para auditoría inmutable.

## 1) Preparar el entorno (sin internet)
```bash
python -m venv .venv
source .venv/bin/activate
pip install --no-cache-dir -r requirements.offline.txt
```

## 2) Variables mínimas
```bash
export PRAETOR_LOG_DIR=data/logs
```

## 3) Encender Praetor
```bash
PYTHONPATH=src uvicorn src.praetor.main:app --host 127.0.0.1 --port 8000
```
Déjalo corriendo; solo registra, no bloquea.

## 4) Registrar una consulta al LLM
```bash
curl -X POST http://127.0.0.1:8000/v1/log \
  -H 'Content-Type: application/json' \
  -d '{
    "action": "chat/query",
    "agent_id": "usuario1",
    "prompt": "¿Cuál es la situación?",
    "response": "Respuesta del LLM",
    "classification": "PUBLICA",
    "metadata": {}
  }'
```

**Response:**
```json
{
  "status": "logged",
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f",
  "timestamp": "2026-04-13T15:26:27Z"
}
```

## 5) Verificar logs
Los eventos se guardan automáticamente en `data/logs/2026-04-13.log`.

```bash
# Ver último evento
tail -n 1 data/logs/2026-04-13.log | jq .
```

Cada línea es un JSON con evento + hash encadenado. Si alguien modifica un evento anterior, la cadena se rompe inmediatamente.

Listo: tienes un libro de bitácora digital inmutable, sin fricción ni dependencias externas.
