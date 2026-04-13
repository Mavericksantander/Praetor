"""
Logger con hash encadenado para auditoría inmutable.
Cada evento se registra con SHA-256 encadenado.
"""

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

from .config import settings


class EventLogger:
    """Registrador de eventos con integridad criptográfica."""
    
    def __init__(self, log_dir: Path | None = None):
        self.log_dir = log_dir or settings.log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_today_log_path(self) -> Path:
        """Retorna ruta del log del día actual."""
        today = dt.datetime.utcnow().strftime("%Y-%m-%d")
        return self.log_dir / f"{today}.log"
    
    def _get_previous_hash(self) -> str:
        """Lee el hash del último evento registrado."""
        path = self._get_today_log_path()
        
        if not path.exists():
            return "0" * 64  # Hash inicial
        
        try:
            with path.open("r", encoding="utf-8") as f:
                last_line = None
                for line in f:
                    if line.strip():
                        last_line = line
                
                if last_line:
                    last_event = json.loads(last_line)
                    return last_event.get("hash", "0" * 64)
        except Exception:
            pass
        
        return "0" * 64
    
    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        """
        Registra un evento con hash encadenado.
        
        Retorna el evento completo con hash y previous_hash.
        """
        timestamp = dt.datetime.utcnow().isoformat() + "Z"
        previous_hash = self._get_previous_hash()
        
        # Construir evento con timestamp
        complete_event = {
            "timestamp": timestamp,
            **event,
        }
        
        # Calcular hash: SHA256(previous_hash + evento_json)
        event_json = json.dumps(complete_event, sort_keys=True, ensure_ascii=False)
        hash_input = (previous_hash + event_json).encode("utf-8")
        event_hash = hashlib.sha256(hash_input).hexdigest()
        
        # Agregar hashes al evento
        complete_event["previous_hash"] = previous_hash
        complete_event["hash"] = event_hash
        
        # Escribir en archivo
        path = self._get_today_log_path()
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(complete_event, ensure_ascii=False) + "\n")
        
        return complete_event
