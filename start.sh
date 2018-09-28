#!/bin/bash

sleep 3
cd ~/CEID-Display/
python3 ./server.py &
sleep 3
python3 ./server.py &
sleep 3
chromium-browser --app=http://localhost:5000 --start-fullscreen
