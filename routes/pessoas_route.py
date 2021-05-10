from app import app, db
from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from modelos.pessoa import Pessoa
from modelos.carro import Carro


@app.route("/tabelas/pessoas", methods=['GET', 'POST'])
def tabela_pessoas():

    if request.method == 'GET':
        pessoas =Pessoa.getPessoas()
        return render_template('tabelas/pessoas.html', pessoas=pessoas)
    elif request.method == 'POST':

        data = request.form
        nome = data.get("nome")
        cpf = data.get("cpf")
        data_nascimento = data.get("data_nascimento")
        celular = data.get("celular")
        email = data.get("email")
        sexo = data.get("sexo")

        try:
            pessoa = Pessoa(
                nome=nome,
                data_nascimento=data_nascimento,
                email=email,
                sexo=sexo,
                celular=celular,
                cpf=cpf,
            )
            print('pessoa', pessoa.serialize())
            db.session.add(pessoa)
            db.session.commit()
            pessoas = Pessoa.getPessoas()
            return render_template('tabelas/pessoas.html',
                                   feedback="Pessoa adicionada com sucesso!",
                                   pessoas=pessoas)
        except Exception as e:
            return (str(e))


@app.route('/remove/pessoa', methods=['POST'])
def remove_pessoa():
    data = request.form
    pessoa = Pessoa.query.get(data.get('id'))
    db.session.delete(pessoa)
    db.session.commit()
    strID = str(data.get('id'))
    feedback = "Pessoa removida com sucesso com sucesso! ID: " + strID
    return render_template('tabelas/pessoas.html',
                           feedback=feedback,
                           pessoas=Pessoa.getPessoas())


@app.route('/editar/pessoa/<id>', methods=['GET', 'POST'])
def edit_pessoa(id):
    if request.method == 'GET':
        pessoa = Pessoa.query.get(id)
        return render_template('tabelas/pessoas.html',
                               pessoas=Pessoa.getPessoas(),
                               pessoa=pessoa.serialize(),
                               edit=True)
    if request.method == 'POST':
        data = request.form
        if request.form['submit'] == 'fechar':
            return render_template(
                'tabelas/pessoas.html',
                pessoas=Pessoa.getPessoas(),
            )
        elif request.form['submit'] == 'editar':
            pessoa = Pessoa.query.get(id)
            print('sexo', pessoa.sexo)
            pessoa.nome = data.get("nome")
            pessoa.celular = data.get("celular")
            pessoa.data_nascimento = data.get("data_nascimento")
            pessoa.email = data.get("email")
            pessoa.sexo = data.get("sexo")
            pessoa.cpf = data.get("cpf")
            db.session.commit()

            return render_template('tabelas/pessoas.html',
                                   pessoas=Pessoa.getPessoas(),
                                   feedback='Pessoa editada com sucesso!',
                                   edit=False)


