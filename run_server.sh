#!/usr/bin/env bash
# =========================================================
# Run Script for Kamleshvar's Birthday Archive
# Supports custom PORT and HOST environment variables
# =========================================================

set -e

PORT="${PORT:-1051}"
HOST="${HOST:-0.0.0.0}"
WORKERS="${WORKERS:-2}"

echo "========================================================"
echo "🎂 Starting Kamleshvar Birthday Archive Server"
echo "📍 Address: http://${HOST}:${PORT}"
echo "========================================================"

# Activate virtual environment if present
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run with Gunicorn if installed, else fallback to Flask's built-in server
if command -v gunicorn &> /dev/null; then
    echo "⚡ Running with Gunicorn (${WORKERS} workers) on ${HOST}:${PORT}..."
    exec gunicorn --workers "${WORKERS}" --bind "${HOST}:${PORT}" --timeout 120 main:app
else
    echo "⚡ Running with Python Flask on ${HOST}:${PORT}..."
    export HOST="${HOST}"
    export PORT="${PORT}"
    exec python3 main.py
fi
