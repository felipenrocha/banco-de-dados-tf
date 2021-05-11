from app import app, db
from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from modelos.tipo_uber import TipoUber



@app.route("/tabelas/tipo_uber", methods=['GET', 'POST'])
def tabela_tipo_uber ():

    if request.method == 'GET':
        tipo_ubers  = getTipoUbers()
        return render_template('tabelas/tipo_uber.html', tipo_ubers=tipo_ubers )
    elif request.method == 'POST':

        data = request.form
        nome = data.get("nome")
        multiplicador = data.get("multiplicador")

        try:
            tipo_uber = TipoUber(nome=nome,multiplicador= multiplicador)
            db.session.add(tipo_uber)
            db.session.commit()
            tipo_uber  = getTipoUbers()
            return render_template('tabelas/tipo_uber.html',
                                   feedback="TipoUber adicionado com sucesso!",
                                   tipo_ubers =tipo_uber )
        except Exception as e:
            return (str(e))


@app.route('/remove/tipo_uber', methods=['POST'])
def remove_uber():
    data = request.form
    # print('data',data , 'id', data['id'])
    tipo_uber = TipoUber.query.get(data.get('id'))
    db.session.delete(tipo_uber)
    db.session.commit()
    strID = str(data.get('id'))
    feedback = "TipoUber removido com sucesso com sucesso! ID: " + strID
    return render_template('tabelas/tipo_uber.html',
                           feedback=feedback,
                           tipo_ubers=getTipoUbers())


@app.route('/editar/tipo_uber/<id>', methods=['GET', 'POST'])
def edit_uber(id):
    if request.method == 'GET':
        tipo_uber = TipoUber.query.get(id)
        return render_template('tabelas/tipo_uber.html',
                               tipo_ubers =getTipoUbers(),
                               tipo_uber=tipo_uber.serialize(),
                               edit=True)
    if request.method == 'POST':
        data = request.form
        if request.form['submit'] == 'fechar':
            return render_template(
                'tabelas/tipo_uber.html',
                tipo_ubers=getTipoUbers(),
            )
        elif request.form['submit'] == 'editar':
            tipo_uber = TipoUber.query.get(id)
            tipo_uber.nome = data.get("nome")
            tipo_uber.multiplicador = data.get("multiplicador")
            db.session.commit()

            return render_template('tabelas/tipo_uber.html',
                                   tipo_ubers=getTipoUbers(),
                                   feedback= 'TipoUber editado com sucesso!',
                                   edit=False)


def getTipoUbers():
    tipo_ubersQuery  = TipoUber.query.all()
    tipo_ubers  = list()
    for e in tipo_ubersQuery:
        tipo_ubers.append(e.serialize())
    return tipo_ubers
