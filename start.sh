#!/bin/bash

cd ~/CEID-Display/
sleep 60		# give it a minute to get internet
python3 ./server.py &
sleep 3			# give it a few seconds to start the server
chromium-browser --app=http://localhost:5000 --start-fullscreen &
