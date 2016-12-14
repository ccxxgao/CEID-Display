#!/bin/bash

cd ~/CEID-Display/
python3 ./server.py &
sleep 3
chromium-browser --app=http://localhost:5000 --start-fullscreen &
