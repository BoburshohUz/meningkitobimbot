#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then python -m venv .venv; fi
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if command -v alembic >/dev/null; then alembic upgrade head || true; fi

if [ "${WORKERS:-0}" -eq 1 ] && command -v celery >/dev/null; then
    celery -A app.tasks.push_notifications.celery_app worker --loglevel=INFO &
fi

PORT=${PORT:-8000}
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
