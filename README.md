# Praetor Gateway

**Auditoría inmutable con integridad criptográfica para LLM del Ejército de Chile.**

## Propósito

Praetor registra cada consulta a un LLM con hash SHA-256 encadenado, garantizando integridad y trazabilidad sin interferir con operaciones.

## Requisitos

- Python 3.11+
- pip

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.offline.txt
```

## Uso

### Iniciar Praetor

```bash
export PRAETOR_LOG_DIR=data/logs
uvicorn src.praetor.main:app --host 127.0.0.1 --port 8000
```

### Registrar una consulta al LLM

```bash
curl -X POST http://127.0.0.1:8000/v1/log \
  -H 'Content-Type: application/json' \
  -d '{
    "action": "chat/query",
    "classification": "PUBLICA",
    "agent_id": "usuario_1",
    "prompt": "¿Cuál es la situación?",
    "response": "Respuesta del LLM...",
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

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

## Archivos de Log

Los eventos se registran en:

```
data/logs/2026-04-13.log
data/logs/2026-04-14.log
```

Cada línea es un JSON con el evento completo + hash encadenado.

### Verificar Integridad

Cada evento contiene:
- `hash`: SHA-256 del evento actual
- `previous_hash`: SHA-256 del evento anterior

**Para verificar que no hubo tampering:**

```bash
# Leer último evento
tail -n 1 data/logs/2026-04-13.log | jq .

# Si alguien modificó un evento anterior, la cadena se rompe inmediatamente.
```

## Variables de Entorno

- `PRAETOR_LOG_DIR`: Directorio para logs (default: `data/logs`)

## Estructura

```
src/praetor/
├── main.py      # API FastAPI
├── logger.py    # Lógica de hash encadenado
└── config.py    # Configuración
```

## Roadmap

- **v0.1.0**: Auditoría con hash encadenado (actual)
- **v0.2.0**: Verificación de integridad
- **v0.3.0**: Exportación de reportes
- **v1.0.0**: HMAC/mTLS

## Licencia

Apache 2.0
