"""
Praetor Gateway: API minimalista para auditoría con hash encadenado.
"""

import socket
import uuid
from typing import Any, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .logger import EventLogger
from .config import settings

app = FastAPI(
    title="Praetor Gateway",
    version="0.1.0",
    description="Auditoría inmutable para LLM del Ejército de Chile",
)

logger = EventLogger(settings.log_dir)


class LogRequest(BaseModel):
    """Solicitud mínima para registrar un evento."""

    action: str = Field(..., description="Tipo de acción (ej: chat/query)")
    agent_id: str = Field(..., description="Identificación del usuario/agente")
    prompt: str = Field(..., description="Mensaje enviado al LLM")
    response: str = Field(..., description="Respuesta del LLM")
    classification: Optional[str] = Field(
        default=None,
        description="Etiqueta opcional de clasificación (texto libre)",
    )
    metadata: Optional[dict[str, Any]] = Field(default_factory=dict)


class LogResponse(BaseModel):
    """Respuesta con evidencia de auditoría."""
    status: str
    event_id: str
    hash: str
    timestamp: str


@app.get("/health")
def health():
    """Health check."""
    return {
        "status": "ok",
        "service": "praetor",
        "version": "0.1.0",
    }


@app.post("/v1/log", response_model=LogResponse)
def log_event(payload: LogRequest) -> LogResponse:
    """
    Registra un evento con hash encadenado e integridad criptográfica.

    Cada evento se almacena en un archivo de log diario con SHA-256 encadenado.
    """
    
    # Generar ID único
    event_id = str(uuid.uuid4())
    hostname = socket.gethostname()
    
    # Construir evento
    event = {
        "event_id": event_id,
        "hostname": hostname,
        "agent_id": payload.agent_id,
        "action": payload.action,
        "classification": payload.classification,
        "prompt": payload.prompt,
        "response": payload.response,
        "metadata": payload.metadata,
    }
    
    # Registrar con hash encadenado
    logged_event = logger.append(event)
    
    return LogResponse(
        status="logged",
        event_id=event_id,
        hash=logged_event["hash"],
        timestamp=logged_event["timestamp"],
    )
