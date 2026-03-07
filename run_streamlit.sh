#!/bin/bash
set -e

# Check streamlit
if ! command -v streamlit >/dev/null 2>&1; then
    echo "streamlit isn't installed. please run 'pip install -r requirements.txt' first."
    exit 1
fi

# Use current dir
cd "$(dirname "$0")"

# Default port (can override with first argument)
PORT=${1:-8501}

# Start streamlit in background
nohup streamlit run streamlit_app.py --server.port="$PORT" "${@:2}" > streamlit.log 2>&1 &

echo "Streamlit server started on port $PORT (pid $!). logs -> $(pwd)/streamlit.log"