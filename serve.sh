#! /bin/bash

if [ "$EUID" -ne 0 ]
  then echo "run as root"
  exit
fi

python3 html_server.py &
HTML_PID=$!
python3 ws_server.py &
WS_PID=$!

trap 'kill $HTML_PID; kill $WS_PID; exit' SIGINT
echo 'HTML and WS servers running'
sleep infinity
