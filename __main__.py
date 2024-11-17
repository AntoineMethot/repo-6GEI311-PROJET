from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__,template_folder='templates', static_folder='static') ##Instanciation de la classe flask

API_KEY = '58902d1c73fc275d3d013f26d76de5bd'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
units = 'metric'

@app.route("/")
def Home():
    get_Weather()
    return render_template('index.html')

@app.route("/get_Weather", methods=['GET'])
def get_Weather():
    # Get the city from the query parameter, defaulting to 'Chicoutimi'
    city = request.args.get('city', 'Chicoutimi')

    # Construct the API URL with the correct parameters
    apiURL = f'{BASE_URL}?q={city}&appid={API_KEY}&units=metric'  # Adjust 'units' as necessary

    # Send the GET request to OpenWeatherMap
    response = requests.get(apiURL)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        weather_data = response.json()
        weather_data = json.load(weather_data)

        print(weather_data[0])


    else:
        return jsonify({'error': 'Failed to fetch weather data'}), 500


if __name__ == '__main__':        ##Permet de lancer notre site web flask
    app.run(debug=True)