#!/bin/bash
cd "$(dirname "$0")/.."

cd hyderabad
nohup python ../hyderabad/manage.py runserver_plus 0.0.0.0:8001 --cert-file cert.pem --key-file key.pem > hyderabad.log 2>&1 &

cd ../kochi
nohup python ../kochimanage.py runserver_plus 0.0.0.0:8002 --cert-file cert.pem --key-file key.pem > kochi.log 2>&1 &
