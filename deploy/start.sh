#!/bin/bash
set -e

# Set internal gateway port
export API_SERVER_PORT=8642
export API_SERVER_ENABLED=true
export HERMES_GATEWAY_PORT=8642

echo "[*] Starting Hermes Agent Gateway in background..."
# Run hermes gateway in the background
hermes gateway run &
HERMES_PID=$!

echo "[*] Starting On-Server Web Chat proxy on port ${PORT:-10000}..."
python3 /opt/hermes/deploy/server.py &
PROXY_PID=$!

# Wait for both processes
trap "kill $HERMES_PID $PROXY_PID" SIGINT SIGTERM
wait -n
