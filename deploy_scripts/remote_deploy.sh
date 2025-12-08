#!/usr/bin/env bash
# remote_deploy.sh <zip-file>
set -euo pipefail

ZIPFILE="${1:-kids-reads-app.zip}"
DEPLOY_BASE_DIR="$(pwd)"
APP_DIR="${DEPLOY_BASE_DIR}/app_deploy"

echo "Starting remote deploy: ${ZIPFILE} into ${APP_DIR}"
mkdir -p "${APP_DIR}"
TMPDIR="${APP_DIR}_tmp_$(date +%s)"
mkdir -p "${TMPDIR}"
unzip -oq "${ZIPFILE}" -d "${TMPDIR}"

# Sync files, preserve uploads and instance if present
rsync -a --delete --exclude 'instance/' --exclude 'uploads/' "${TMPDIR}/" "${APP_DIR}/"

mkdir -p "${APP_DIR}/uploads"
chmod 755 "${APP_DIR}/uploads"

VENV_DIR="${APP_DIR}/venv"
PYTHON_BIN="${VENV_DIR}/bin/python3"

if [ ! -x "${PYTHON_BIN}" ]; then
  echo "Creating virtualenv..."
  python3 -m venv "${VENV_DIR}"
fi

echo "Activating virtualenv and installing requirements..."
source "${VENV_DIR}/bin/activate"
pip install --upgrade pip
if [ -f "${APP_DIR}/requirements.txt" ]; then
  pip install -r "${APP_DIR}/requirements.txt"
fi

# Run init_db to ensure tables and seed users exist
if [ -f "${APP_DIR}/init_db.py" ]; then
  echo "Running init_db.py (may seed users)..."
  "${PYTHON_BIN}" "${APP_DIR}/init_db.py" || true
fi

chown -R $(whoami):$(whoami) "${APP_DIR}"
chmod -R u+rwX "${APP_DIR}"

SERVICE_NAME="kids-reads"
if systemctl --no-pager status "${SERVICE_NAME}" >/dev/null 2>&1; then
  echo "Restarting ${SERVICE_NAME} service..."
  sudo systemctl daemon-reload || true
  sudo systemctl restart "${SERVICE_NAME}"
  sudo systemctl status "${SERVICE_NAME}" --no-pager || true
else
  echo "Service ${SERVICE_NAME} not found. Deployment finished copying files to ${APP_DIR}."
fi

rm -rf "${TMPDIR}"
echo "Deploy finished."
