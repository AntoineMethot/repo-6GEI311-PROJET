from flask import Flask, render_template, request, jsonify

app = Flask(__name__,template_folder='templates', static_folder='static') ##Instanciation de la classe flask

API_KEY = '58902d1c73fc275d3d013f26d76de5bd'
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route("/")
def Home():
    return render_template('index.html')

@app.route("/getWeather")
def getWeather():
    return()

if __name__ == '__main__':        ##Permet de lancer notre site web flask
    app.run(debug=True)