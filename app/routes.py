import requests
import boto3
import json
from datetime import datetime
from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

API_KEY = "c1231ea55d2c043fce682386b5151ce6"

# --- S3 Setup ---
s3 = boto3.client('s3')
BUCKET_NAME = "weather-data-primary"

def upload_weather_to_s3(weather_data, city):
    """Uploads weather data JSON to S3 with timestamped filename."""
    file_name = f"{city}_{datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(weather_data),
        ContentType="application/json"
    )
    print(f"✅ Uploaded {file_name} to S3")

@main.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        print("API URL:", url)
        print("API Response:", response.status_code, response.text)

        if response.status_code == 200:
            data = response.json()
            weather = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }

            # Upload to S3
            upload_weather_to_s3(weather, city)

        else:
            weather = 'not found'

    return render_template('index.html', weather=weather)

