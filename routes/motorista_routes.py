from app import app, db
from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from modelos.motorista import Motorista
from modelos.carro import Carro
from modelos.pessoa import Pessoa


@app.route("/tabelas/motoristas", methods=['GET', 'POST'])
def tabela_motoristas():

    if request.method == 'GET':
        motoristas = getMotoristas()
        return render_template('tabelas/motoristas.html',
                               motoristas=motoristas)
    elif request.method == 'POST':

        data = request.form
        cpf = data['cpf']
        try:
            pessoa = Pessoa.getPessoaByCPF(cpf)
            motorista = Motorista(pessoa_id=pessoa.id)
            print('motorista', motorista.serialize())
            db.session.add(motorista)
            db.session.commit()
            motoristas = getMotoristas()
            return render_template(
                'tabelas/motoristas.html',
                feedback="Motorista adicionado com sucesso!",
                motoristas=motoristas)
        except Exception as e:
            render_template('tabelas/motoristas.html',
                           feedback=str(e),
                            motoristas=motoristas)


@app.route('/remove/motorista', methods=['POST'])
def remove_motorista():
    data = request.form
    # print('data',data , 'id', data['id'])
    motorista = Motorista.query.get(data.get('id'))
    db.session.delete(motorista)
    db.session.commit()
    strID = str(data.get('id'))
    feedback = "Motorista removido com sucesso com sucesso! ID: " + strID
    return render_template('tabelas/motoristas.html',
                           feedback=feedback,
                           motoristas=getMotoristas())



def getCarroByPlaca(placa):
    """"
        Função p/ retornar o carro baseado na placa do cliente
    """
    carro = Carro.query.filter_by(placa=placa).first()
    return carro


def getMotoristas():
    motoristasObjects = Motorista.query.all()
    motoristas = list()
    for e in motoristasObjects:
        motoristas.append(e.serialize())
    return motoristas
