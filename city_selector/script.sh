#!/bin/bash

echo "Starting Django servers in the background..."

# Get the local network IP
IP=$(hostname -I | awk '{print $1}')

# Start city_selector server and store PID
nohup python3 /home/deeks/Desktop/Projects/metro/city_selector/manage.py runserver 0.0.0.0:8000 &> city_selector.log &
echo $! > city_selector.pid

# Start Hyderabad server and store PID
nohup python3 /home/deeks/Desktop/Projects/metro/hyderabad/manage.py runserver_plus 0.0.0.0:8001 --cert-file cert.pem --key-file key.pem &> hyderabad.log &
echo $! > hyderabad.pid

# Start Kochi server and store PID
nohup python3 /home/deeks/Desktop/Projects/metro/kochi/manage.py runserver_plus 0.0.0.0:8002 --cert-file cert.pem --key-file key.pem &> kochi.log &
echo $! > kochi.pid

echo "All servers started successfully!"

# Loop to display server URLs
echo "Press Ctrl+C to stop all servers..."
while true; do
    echo "http://$IP:8000"
    sleep 4
done
