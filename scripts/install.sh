#!/usr/bin/env bash
set -euo pipefail

# Simple installer for Praetor (local LLM auditing)
# Usage: curl -sSL https://raw.githubusercontent.com/Mavericksantander/Praetor/main/scripts/install.sh | bash

INSTALL_DIR="/opt/praetor"
SERVICE_NAME="praetor"
PYTHON_BIN=${PYTHON_BIN:-"python3"}
PORT=${PORT:-8000}
HOST=${HOST:-127.0.0.1}
LOG_DIR=${PRAETOR_LOG_DIR:-"/var/praetor/logs"}
REPO_URL="https://github.com/Mavericksantander/Praetor.git"

require_root() {
  if [ "$(id -u)" -ne 0 ]; then
    echo "[!] Ejecuta como root o con sudo: este instalador escribe en /opt y /etc/systemd." >&2
    exit 1
  fi
}

install_deps() {
  command -v $PYTHON_BIN >/dev/null || { echo "[!] Se requiere Python 3"; exit 1; }
  command -v git >/dev/null || { echo "[!] Se requiere git"; exit 1; }
  command -v systemctl >/dev/null || { echo "[!] Se requiere systemd"; exit 1; }
}

clone_repo() {
  rm -rf "$INSTALL_DIR"
  git clone "$REPO_URL" "$INSTALL_DIR"
}

create_venv() {
  cd "$INSTALL_DIR"
  $PYTHON_BIN -m venv .venv
  source .venv/bin/activate
  pip install --no-cache-dir -r requirements.offline.txt
}

prepare_dirs() {
  mkdir -p "$LOG_DIR"
  chown -R $(id -u):$(id -g) "$LOG_DIR"
}

create_service() {
  cat > /etc/systemd/system/${SERVICE_NAME}.service <<SERVICE
[Unit]
Description=Praetor Gateway
After=network.target

[Service]
Type=simple
WorkingDirectory=$INSTALL_DIR
Environment=PRAETOR_LOG_DIR=$LOG_DIR
ExecStart=$INSTALL_DIR/.venv/bin/uvicorn src.praetor.main:app --host $HOST --port $PORT
Restart=on-failure
User=$(id -un)
Group=$(id -gn)

[Install]
WantedBy=multi-user.target
SERVICE
  systemctl daemon-reload
  systemctl enable ${SERVICE_NAME}.service
  systemctl restart ${SERVICE_NAME}.service
}

main() {
  require_root
  install_deps
  clone_repo
  create_venv
  prepare_dirs
  create_service
  echo "[+] Praetor instalado y corriendo en http://${HOST}:${PORT}"
  echo "    Logs: $LOG_DIR"
}

main "$@"
