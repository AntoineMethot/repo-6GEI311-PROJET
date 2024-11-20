from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__, template_folder='templates', static_folder='static') ##Instanciation de la classe flask

API_KEY = '58902d1c73fc275d3d013f26d76de5bd'
CURRENT_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall'
TESTER_BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast/daily'
units = 'metric'

@app.route("/", methods=['GET', 'POST'])
def Home():
    city = 'Chicoutimi'  # Default city
    weather_data = None
    forecast_data = None

    if request.method == 'POST':
        # Get the city name from the form input
        city = request.form.get('city', 'Chicoutimi')

    # Construct the API URL
    CURRENT_api_url = f"{CURRENT_BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    CURRENT_response = requests.get(CURRENT_api_url)

    if CURRENT_response.status_code == 200:
        # Parse the JSON response if successful
        weather_data = CURRENT_response.json()
        print(weather_data)
    else:
        weather_data = {"error": "Could not fetch weather data. for the entered city. Please enter another city"}

    #FORECAST_api_url = f"{FORECAST_BASE_URL}?q={city}&appid={API_KEY}&units={units}&exclude=current,minutely,hourly"
    FORECAST_api_url = f"{TESTER_BASE_URL}?q={city}&cnt={7}&appid={API_KEY}"
    FORECAST_response= requests.get(FORECAST_api_url)

    if FORECAST_response.status_code == 200:
        # Parse the JSON response if successful
        forecast_data = FORECAST_response.json()
        print(forecast_data)
    else:
        forecast_data = {"error": "Could not fetch forecast data. for the entered city. Please enter another city"}
        print(forecast_data)
        print(FORECAST_response.status_code)


    # Pass the weather data and city name to the template
    return render_template("index.html", city=city, weather_data=weather_data)


if __name__ == '__main__':        ##Permet de lancer notre site web flask
    app.run(host='0.0.0.0',debug=True)