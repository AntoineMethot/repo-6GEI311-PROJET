from flask import Flask, render_template

app = Flask(__name__,template_folder='templates', static_folder='static') ##Instanciation de la classe flask

@app.route("/")
def Home():
    return render_template('index.html')

if __name__ == '__main__':        ##Permet de lancer notre site web flask
    app.run(debug=True)