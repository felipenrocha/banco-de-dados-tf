from app import app, db
from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from modelos.carro import Carro
from modelos.tipo_uber import TipoUber
from modelos.motorista import Motorista


@app.route("/tabelas/carros", methods=['GET', 'POST'])
def tabela_carros():

    if request.method == 'GET':
        carros = getCarros()
        return render_template('tabelas/carros.html', carros=carros, tipos_uber=TipoUber.getAll())
    elif request.method == 'POST':
        data = request.form
        cpf_motorista = data.get('cpf')
        modelo = data.get("modelo")
        cor = data.get("cor")
        chassi = data.get("chassi")
        placa =  data.get("placa")
        marca = data.get("marca")
        ano = data.get("ano")
        tipo_uber_id = data.get("tipo_uber")

        try:
            motorista = Motorista.getMotoristaByCPF(cpf=cpf_motorista).serialize()
            carro = Carro(modelo=modelo, chassi=chassi, marca=marca, ano=ano, placa=placa, cor= cor, tipo_uber_id=tipo_uber_id, motorista_id=motorista['id'])
            db.session.add(carro)
            db.session.commit()
            carros = getCarros()
            return render_template('tabelas/carros.html',
                                   feedback="Carro adicionado com sucesso!",
                                   carros=carros, tipos_uber=TipoUber.getAll())
        except Exception as e:
            return (str(e))


@app.route('/remove/carro', methods=['POST'])
def remove_car():
    data = request.form
    # print('data',data , 'id', data['id'])
    carro = Carro.query.get(data.get('id'))
    db.session.delete(carro)
    db.session.commit()
    strID = str(data.get('id'))
    feedback = "Carro removido com sucesso com sucesso! ID: " + strID
    return render_template('tabelas/carros.html',
                           feedback=feedback,
                           carros=getCarros())


@app.route('/editar/carro/<id>', methods=['GET', 'POST'])
def edit_car(id):
    if request.method == 'GET':
        carro = Carro.query.get(id)
        return render_template('tabelas/carros.html',
                               carros=getCarros(),
                               carro=carro.serialize(),
                               edit=True, tipos_uber=TipoUber.getAll())
    if request.method == 'POST':
        data = request.form
        if request.form['submit'] == 'fechar':
            return render_template(
                'tabelas/carros.html',
                carros=getCarros(),
            )
        elif request.form['submit'] == 'editar':
            carro = Carro.query.get(id)
            carro.modelo = data.get("modelo")
            carro.placa =  data.get("placa")
            carro.chassi = data.get("chassi")
            carro.marca = data.get("marca")
            carro.ano = data.get("ano")
            carro.tipo_uber_id = None
            carro.tipo_uber_id = data.get("tipo_uber")
            carro.cor = data.get("cor")
            db.session.commit()

            return render_template('tabelas/carros.html',
                                   carros=getCarros(),
                                   feedback= 'Carro editado com sucesso!',
                                   edit=False, tipos_uber=TipoUber.getAll())


def getCarros():
    carrosObjects = Carro.query.all()
    carros = list()
    for e in carrosObjects:
        carros.append(e.serialize())
    return carros
