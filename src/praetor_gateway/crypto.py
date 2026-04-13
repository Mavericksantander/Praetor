"""
Funciones de firma reducidas a no-op para la versión mínima del gateway.
Se mantienen para compatibilidad de importaciones.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional


def sign_path(path: Path) -> Optional[str]:
    """No-op: devuelve None sin modificar el archivo."""
    return None
