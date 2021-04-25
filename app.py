from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # objeto para administrar o banco de dados;

from modelos.carro import Carro
from modelos.tipo_uber import TipoUber
from modelos.motorista import Motorista
from modelos.cliente import Cliente
from modelos.viagem import Viagem




@app.route("/")
def home():
    return render_template('sgbd.html')


# @app.route("/tabelas")
# def sgbd():
#     return render_template('sgbd.html')

mapbox_access_token = 'pk.eyJ1IjoiZmVsaXBlbnJvY2hhIiwiYSI6ImNrbnhlYjU2eTByNnkycHM1Z3l0ZW9vMW8ifQ.HX0v32fjRqNf5clZ-zx65w'


from routes import carros_routes, tipo_uber_routes, motorista_routes, cliente_routes, viagem_routes


if __name__ == '__main__':
    app.run()