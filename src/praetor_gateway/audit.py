from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, Optional

from .config import settings

class AuditLog:
    def __init__(self, path: Path | None = None):
        self.path = path or settings.audit_log_path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _last_hash(self) -> str:
        if not self.path.exists():
            return "0" * 64
        with self.path.open("r", encoding="utf-8") as f:
            last = None
            for line in f:
                if line.strip():
                    last = line
        if not last:
            return "0" * 64
        record = json.loads(last)
        return record.get("hash", "0" * 64)

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        now = dt.datetime.utcnow().isoformat() + "Z"
        payload = {
            "timestamp": now,
            **event,
        }
        previous_hash = self._last_hash()
        payload_str = json.dumps(payload, sort_keys=True)
        hash_value = hashlib.sha256((previous_hash + payload_str).encode("utf-8")).hexdigest()
        payload.update({"previous_hash": previous_hash, "hash": hash_value})
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
        return payload

    def export_lines(self, since: Optional[dt.datetime] = None) -> list[str]:
        if not self.path.exists():
            return []
        lines: list[str] = []
        if since and since.tzinfo is None:
            since = since.replace(tzinfo=dt.timezone.utc)
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                ts = dt.datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))
                if since and ts < since:
                    continue
                lines.append(line.rstrip())
        return lines
