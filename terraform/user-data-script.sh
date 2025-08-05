#!/bin/bash

# Update package list and install dependencies
sudo apt update -y
sudo apt install -y python3 python3-pip git

# Clone your weather tracker app from GitHub
git clone https://github.com/tushardubey/weather_app.git /home/ubuntu/weather-app

# Navigate to app directory
cd /home/ubuntu/weather-app

# OPTIONAL: install dependencies (if you have requirements.txt, use it)
pip3 install -r requirements.txt

# If not, install Flask manually
pip3 install flask

# Run the Flask app using run.py
nohup python3 run.py > app.log 2>&1 &
