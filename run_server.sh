#!/usr/bin/env bash
# =========================================================
# Run Script for Kamleshvar's Birthday Archive (Raspberry Pi 5 Ready)
# Exposes as a single port (default 5000)
# =========================================================

set -e

PORT="${PORT:-5000}"
HOST="${HOST:-0.0.0.0}"
WORKERS="${WORKERS:-4}"

echo "========================================================"
echo "🎂 Starting Kamleshvar's Birthday Archive Server"
echo "📍 Host: http://${HOST}:${PORT}"
echo "========================================================"

# Activate virtual environment if present
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run with Gunicorn if installed, else fallback to Flask's built-in WSGI server
if command -v gunicorn &> /dev/null; then
    echo "⚡ Running with Gunicorn (${WORKERS} workers) on ${HOST}:${PORT}..."
    exec gunicorn --workers "${WORKERS}" --bind "${HOST}:${PORT}" --timeout 120 main:app
else
    echo "⚡ Running with Python Flask on ${HOST}:${PORT}..."
    export HOST="${HOST}"
    export PORT="${PORT}"
    exec python3 main.py
fi
