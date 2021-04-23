from app import app, db
from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from modelos.cliente import Cliente



@app.route("/tabelas/clientes", methods=['GET', 'POST'])
def tabela_clientes():

    if request.method == 'GET':
        clientes = getClientes()
        return render_template('tabelas/clientes.html',
                               clientes=clientes)
    elif request.method == 'POST':

        data = request.form
        nome = data.get("nome")
        cpf = data.get("cpf")
        data_nascimento = data.get("data_nascimento")
        celular = data.get("celular")
        email = data.get("email")
        sexo = data.get("sexo")

        try:
            cliente = Cliente(nome=nome,
                                  data_nascimento=data_nascimento,
                                  email=email,
                                  sexo=sexo,
                                  celular=celular,
                                  cpf=cpf)
            print('cliente', cliente.serialize())
            db.session.add(cliente)
            db.session.commit()
            clientes = getClientes()
            return render_template(
                'tabelas/clientes.html',
                feedback="Cliente adicionado com sucesso!",
                clientes=clientes)
        except Exception as e:
            return (str(e))


@app.route('/remove/cliente', methods=['POST'])
def remove_cliente():
    data = request.form
    # print('data',data , 'id', data['id'])
    cliente = Cliente.query.get(data.get('id'))
    db.session.delete(cliente)
    db.session.commit()
    strID = str(data.get('id'))
    feedback = "Cliente removido com sucesso com sucesso! ID: " + strID
    return render_template('tabelas/clientes.html',
                           feedback=feedback,
                           clientes=getClientes())


@app.route('/editar/cliente/<id>', methods=['GET', 'POST'])
def edit_cliente(id):
    if request.method == 'GET':
        cliente = Cliente.query.get(id)
        return render_template('tabelas/clientes.html',
                               clientes=getClientes(),
                               cliente=cliente.serialize(),
                               edit=True)
    if request.method == 'POST':
        data = request.form
        if request.form['submit'] == 'fechar':
            return render_template(
                'tabelas/clientes.html',
                clientes=getClientes(),
            )
        elif request.form['submit'] == 'editar':
            cliente = Cliente.query.get(id)
            cliente.nome = data.get("nome")
            cliente.celular = data.get("celular")
            cliente.data_nascimento = data.get("data_nascimento")
            cliente.email = data.get("email")
            cliente.sexo = data.get("sexo")
            cliente.cpf = data.get("cpf")
            db.session.commit()

            return render_template('tabelas/clientes.html',
                                   clientes=getClientes(),
                                   feedback='Cliente editado com sucesso!',
                                   edit=False)



def getClientes():
    clientesObjects = Cliente.query.all()
    clientes = list()
    for e in clientesObjects:
        clientes.append(e.serialize())
    return clientes
