#!/bin/bash


cd ~/CEID-Display/
kill $(cat server_pid)
sleep 5
python3 ./server.py &
echo "Server Reloaded"
