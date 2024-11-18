from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__,template_folder='templates', static_folder='static') ##Instanciation de la classe flask

API_KEY = '58902d1c73fc275d3d013f26d76de5bd'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
units = 'metric'

@app.route("/", methods=['GET', 'POST'])
def Home():
    # Default city
    city = request.form.get('city', 'Chicoutimi')

    # Construct the API URL
    api_url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

    # Fetch the weather data
    weather_data = None
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response if successful
        weather_data = response.json()
        print(weather_data)
    else:
        weather_data = {"error": "Could not fetch weather data. Please try again later."}

    # Pass the weather data and city name to the template
    return render_template("index.html", city=city, weather_data=weather_data)


if __name__ == '__main__':        ##Permet de lancer notre site web flask
    app.run(host='0.0.0.0',debug=True)