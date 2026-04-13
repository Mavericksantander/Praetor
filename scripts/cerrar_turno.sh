#!/usr/bin/env bash
# Sella la bitácora del día (hash SHA-256) por host.
set -euo pipefail
HOSTNAME=$(hostname)
FILE=exports/bitacora/${HOSTNAME}/log_$(date -u +%Y%m%d).txt
if [ ! -f "$FILE" ]; then
  echo "No existe bitácora para hoy: $FILE"
  exit 1
fi
HASH=$(sha256sum "$FILE" | awk '{print $1}')
echo $HASH > "${FILE}.sha256"
echo "Sello generado: ${FILE}.sha256"
echo "Copia ${FILE} y ${FILE}.sha256 a tu medio de custodia (USB)."
