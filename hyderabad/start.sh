#!/bin/bash

# Navigate to the correct directory in WSL
cd /mnt/c/Users/deeks/Desktop/metro_navigation || exit


# Run the Django server with SSL
python3 manage.py runserver_plus 0.0.0.0:8000 --cert-file cert.pem --key-file key.pem
