from flask import Flask, request, jsonify, render_template, redirect
from app import app, db, mapbox_access_token
from modelos.viagem import Viagem, Posicao, Estado
from modelos.motorista import Motorista
from modelos.cliente import Cliente


@app.route('/tabelas/viagens', methods=['GET', 'POST'])
def get():
    if request.method == 'GET':
        return render_template('tabelas/viagens.html',
                               viagens=getViagens(),
                               estados=getEstados(),
                               mapbox_access_token=mapbox_access_token)
    elif request.method == 'POST':
        data = request.form
        valor = calculaValor(2)
        estado = data.get('estado')
        cpf_motorista = data.get('cpf_motorista')
        cpf_cliente = data.get('cpf_cliente')
        motorista_id = Motorista.getMotoristaByCPF(cpf=cpf_motorista).id
        cliente_id = Cliente.getClienteByCPF(cpf=cpf_cliente).id

        viagem = Viagem(valor=valor,
                        estado_id=estado,
                        motorista_id=motorista_id,
                        cliente_id=cliente_id)
        db.session.add(viagem)
        db.session.commit()

        latitude_origem = data.get('posicao_origem_latitude')
        longitude_origem = data.get('posicao_origem_longitude')
        latitude_destino = data.get('posicao_destino_latitude')
        longitude_destino = data.get('posicao_destino_longitude')

        posicao_origem = Posicao(tipo='origem',
                                 latitude=latitude_origem,
                                 longitude=longitude_origem,
                                 viagem_id=viagem.id)
        posicao_destino = Posicao(tipo='destino',
                                  latitude=latitude_destino,
                                  longitude=longitude_destino,
                                  viagem_id=viagem.id)
        db.session.add(posicao_origem)
        db.session.add(posicao_destino)

        db.session.commit()

        return render_template('tabelas/viagens.html',
                               feedback="Viagem adicionada com sucesso!",
                               viagens=getViagens(),
                               estados=getEstados(),
                               mapbox_access_token=mapbox_access_token)


def calculaValor(multiplicador):
    return (25.00 * multiplicador)


def getViagens():
    viagens = list()
    for viagem in Viagem.getAll():
        viagens.append(viagem.serialize())
    return viagens


def getEstados():
    return Estado.getAll()


@app.route('/remove/viagem', methods=['POST'])
def remove_viagem():
    data = request.form
    # print('data',data , 'id', data['id'])
    viagem = Viagem.query.get(data.get('id'))
    db.session.delete(viagem)
    db.session.commit()
    strID = str(data.get('id'))
    feedback = "Viagem removida com sucesso com sucesso! ID: " + strID
    return render_template('tabelas/viagens.html',
                           feedback=feedback,
                           viagens=getViagens(),
                           estados=getEstados(),
                           mapbox_access_token=mapbox_access_token)
