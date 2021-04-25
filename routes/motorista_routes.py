from app import app, db
from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from modelos.motorista import Motorista
from modelos.carro import Carro


@app.route("/tabelas/motoristas", methods=['GET', 'POST'])
def tabela_motoristas():

    if request.method == 'GET':
        motoristas = getMotoristas()
        return render_template('tabelas/motoristas.html',
                               motoristas=motoristas)
    elif request.method == 'POST':

        data = request.form
        nome = data.get("nome")
        cpf = data.get("cpf")
        data_nascimento = data.get("data_nascimento")
        celular = data.get("celular")
        email = data.get("email")
        sexo = data.get("sexo")
        print('getCarroByPlaca(data.get("placa"))', getCarroByPlaca(data.get("placa")).serialize())
        carro_id = getCarroByPlaca(data.get("placa")).id

        try:
            motorista = Motorista(nome=nome,
                                  data_nascimento=data_nascimento,
                                  email=email,
                                  sexo=sexo,
                                  celular=celular,
                                  cpf=cpf,
                                  carro_id=carro_id)
            print('motorista', motorista.serialize())
            db.session.add(motorista)
            db.session.commit()
            motoristas = getMotoristas()
            return render_template(
                'tabelas/motoristas.html',
                feedback="Motorista adicionado com sucesso!",
                motoristas=motoristas)
        except Exception as e:
            return (str(e))


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


@app.route('/editar/motorista/<id>', methods=['GET', 'POST'])
def edit_motorista(id):
    if request.method == 'GET':
        motorista = Motorista.query.get(id)
        return render_template('tabelas/motoristas.html',
                               motoristas=getMotoristas(),
                               motorista=motorista.serialize(),
                               edit=True)
    if request.method == 'POST':
        data = request.form
        if request.form['submit'] == 'fechar':
            return render_template(
                'tabelas/motoristas.html',
                motoristas=getMotoristas(),
            )
        elif request.form['submit'] == 'editar':
            motorista = Motorista.query.get(id)
            print('sexo', motorista.sexo)
            motorista.nome = data.get("nome")
            motorista.celular = data.get("celular")
            motorista.data_nascimento = data.get("data_nascimento")
            motorista.email = data.get("email")
            motorista.sexo = data.get("sexo")
            motorista.cpf = data.get("cpf")
            db.session.commit()

            return render_template('tabelas/motoristas.html',
                                   motoristas=getMotoristas(),
                                   feedback='Motorista editado com sucesso!',
                                   edit=False)



def getCarroByPlaca(placa):
    """"
        Função p/ retornar o carro baseado na placa do cliente
    """
    carro = Carro.query.filter_by(placa=placa).first()
    return carro;

def getMotoristas():
    motoristasObjects = Motorista.query.all()
    motoristas = list()
    for e in motoristasObjects:
        motoristas.append(e.serialize())
    return motoristas
