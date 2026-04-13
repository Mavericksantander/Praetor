from __future__ import annotations

import datetime as dt
import hashlib
import json


class Bitacora:
    """
    Bitácora diaria por host, formato texto con hash encadenado por línea.
    Diseñada para flujo de cambio de guardia: un archivo por día, más hash final.
    """

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path_for_today(self, hostname: str) -> Path:
        today = dt.datetime.utcnow().strftime("%Y%m%d")
        host_dir = self.base_dir / hostname
        host_dir.mkdir(parents=True, exist_ok=True)
        return host_dir / f"log_{today}.txt"

    def append(self, hostname: str, event: dict) -> Path:
        path = self._path_for_today(hostname)
        line = json.dumps(event, ensure_ascii=False)
        prev_hash = "0"
        if path.exists():
            with path.open("rb") as f:
                last = None
                for l in f:
                    if l.strip():
                        last = l
                if last:
                    try:
                        last_obj = json.loads(last)
                        prev_hash = last_obj.get("_hash", "0")
                    except Exception:
                        prev_hash = "0"
        new_hash = hashlib.sha256((prev_hash + line).encode("utf-8")).hexdigest()
        event["_hash"] = new_hash
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        return path
