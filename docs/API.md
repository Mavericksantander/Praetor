# API Praetor

## Endpoint: `POST /v1/log`

Registra un evento de auditoría con hash encadenado.

### Request

```json
{
  "action": "chat/query",
  "classification": "PUBLICA",
  "agent_id": "usuario_1",
  "prompt": "¿Cuál es la situación?",
  "response": "Respuesta del LLM...",
  "metadata": {}
}
```

### Response

```json
{
  "status": "logged",
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f",
  "timestamp": "2026-04-13T15:26:27Z"
}
```

### Clasificaciones Válidas

- `PUBLICA`: Información pública
- `RESERVADO`: Información reservada
- `SECRETO`: Información clasificada

## Endpoint: `GET /health`

Health check del servicio.

### Response

```json
{
  "status": "ok",
  "service": "praetor",
  "version": "0.1.0"
}
```
