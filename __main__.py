from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import json
import sqlite3

app = Flask(__name__, template_folder='templates', static_folder='static') ##Instanciation de la classe flask

API_KEY = '58902d1c73fc275d3d013f26d76de5bd'
CURRENT_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall'
TESTER_BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast/daily'
units = 'metric'

def get_activites():
    conn = sqlite3.connect('Activities.db')
    cursor = conn.cursor()
    query = '''
    SELECT * FROM Activities
    '''

    cursor.execute(query)
    activities = cursor.fetchall()
    conn.close()

    return activities

def recommend_activity(weather_data):
    activities = get_activites()
    current_time = datetime.now().hour
    current_month = datetime.now().month

    if  5 <= current_month <= 10:
        Summer=True
        Winter=False
    elif 1 <= current_month <= 4 or current_month == 11 or current_month == 12:
        Summer=False
        Winter=True
    else:
        Summer= False
        Winter=False


    if weather_data['main']['temp'] >= 15:
        Hot=True
        Cold=False

    elif weather_data['main']['temp'] < 15:
        Cold=True
        Hot=False

    if 'rain' in weather_data['weather']['description'] or 'thunderstorm' in weather_data['weather']['description']:
        Raining =True
    elif 'snow' in weather_data['weather']['description']:
        Snowing = True

    if  6 <= current_time < 17:
        Dark=False
        Light=True
    elif 17 <= current_time < 6:
        Dark=True
        Light=False
    else:
        Dark=False
        Light=True


    recommendations = []

    # Loop through the activities and check if they match the criteria
    for activity in activities:
        activity_name, in_summer, in_winter, when_rain, when_snow, when_hot, when_cold, when_dark, when_light = activity[1], activity[2], activity[3], activity[4], activity[5], activity[6], activity[7], activity[8], activity[9]
        
        # Match conditions based on the flags
        if ((Summer and in_summer) or (Winter and in_winter)) and \
           ((Hot and when_hot) or (Cold and when_cold)) and \
           ((Raining and when_rain) or (Snowing and when_snow)) and \
           ((Light and when_light) or (Dark and when_dark)):
            recommendations.append(activity_name)
    
    # Return the recommendations as JSON
    return json.dumps({"recommended_activities": recommendations})


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

    activities = recommend_activity(weather_data)



    # Pass the weather data and city name to the template
    return render_template("index.html", city=city, weather_data=weather_data, activities=activities)


if __name__ == '__main__':        ##Permet de lancer notre site web flask
    app.run(host='0.0.0.0',debug=True)