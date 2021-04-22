from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # objeto para administrar o banco de dados;

from modelos.carro import Carro
from modelos.tipo_uber import TipoUber

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/tabelas")
def sgbd():
    return render_template('sgbd.html')



from routes import carros_routes, tipo_uber_routes


if __name__ == '__main__':
    app.run()