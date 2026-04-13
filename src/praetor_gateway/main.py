from __future__ import annotations

import datetime as dt
import json
import socket
import uuid
from typing import Any, Optional

from fastapi import FastAPI, Header
from pydantic import BaseModel, Field

from .audit import AuditLog
from .bitacora import Bitacora
from .config import settings

app = FastAPI(title="Praetor Gateway", version="0.1.0")


audit_log = AuditLog()
bitacora = Bitacora(settings.bitacora_dir)


class AuthorizationRequest(BaseModel):
    action: str = Field(..., description="Identificador de la interacción, ej. chat/output")
    classification: Optional[str] = Field(None, description="PUBLICA/RESERVADO/SECRETO")
    agent_id: str = Field(..., description="Identidad o usuario")
    message: Optional[str] = Field(None, description="Contenido enviado al LLM")
    response: Optional[str] = Field(None, description="Respuesta del LLM (opcional si se registra después)")
    metadata: Optional[dict[str, Any]] = Field(default_factory=dict)


class AuthorizationResponse(BaseModel):
    status: str
    log_path: str
    hash: str
    authorization_id: str
    trace_id: str
    incident_id: str


class AuditEvent(BaseModel):
    kind: str
    actor: str
    action: str
    classification: Optional[str] = None
    resource: Optional[str] = None
    details: dict[str, Any] = Field(default_factory=dict)


@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "mode": "bitacora",
    }


@app.post("/v1/authorize", response_model=AuthorizationResponse)
def authorize(payload: AuthorizationRequest, x_request_id: Optional[str] = Header(default=None)):
    trace_id = payload.metadata.get("trace_id") if payload.metadata else None
    if not trace_id:
        trace_id = str(uuid.uuid4())
    authorization_id = str(uuid.uuid4())
    incident_id = str(uuid.uuid4())

    event = {
        "kind": "authorization",
        "actor": payload.agent_id,
        "action": payload.action,
        "classification": payload.classification,
        "metadata": payload.metadata,
        "request_id": x_request_id,
        "allowed": True,
        "require_approval": False,
        "authorization_id": authorization_id,
        "trace_id": trace_id,
        "incident_id": incident_id,
        "hostname": socket.gethostname(),
        "message": payload.message,
        "response": payload.response,
    }
    record = audit_log.append(event)
    bitacora.append(socket.gethostname(), event)
    _write_report(event, record["hash"], authorization_id, incident_id)
    return AuthorizationResponse(
        status="logged",
        hash=record["hash"],
        authorization_id=authorization_id,
        trace_id=trace_id,
        incident_id=incident_id,
        log_path=str(settings.audit_log_path),
    )


@app.post("/v1/audit")
def append_audit(event: AuditEvent):
    record = audit_log.append(event.model_dump())
    return {"status": "recorded", "hash": record["hash"]}



def _write_report(event: dict[str, Any], decision_hash: str, authorization_id: str, incident_id: str) -> None:
    """
    Genera un reporte inmediato por host y query, para uso local/offline.
    """
    hostname = event.get("hostname") or socket.gethostname()
    ts = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    settings.report_dir.mkdir(parents=True, exist_ok=True)
    host_dir = settings.report_dir / hostname
    host_dir.mkdir(parents=True, exist_ok=True)
    report_path = host_dir / f"{ts}_{authorization_id}.json"
    payload = {
        "authorization_id": authorization_id,
        "incident_id": incident_id,
        "timestamp": ts,
        "decision_hash": decision_hash,
        "event": event,
    }
    report_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
