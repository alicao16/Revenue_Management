#!/bin/bash

# simple helper script to start the streamlit app in the background
# usage: ./run_streamlit.sh &
# make executable: chmod +x run_streamlit.sh

set -e

if ! command -v streamlit >/dev/null 2>&1; then
    echo "streamlit isn't installed. please run 'pip install -r requirements.txt' first."
    exit 1
fi

# use the current directory as working directory
cd "$(dirname "$0")"

# write log to file
nohup streamlit run streamlit_app.py --server.port=8501 "${@}" > streamlit.log 2>&1 &

echo "Streamlit server started (pid $!). logs -> $(pwd)/streamlit.log"
