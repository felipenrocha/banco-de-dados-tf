from flask import Flask, request, jsonify, render_template, redirect
from app import app, db, mapbox_access_token
from modelos.viagem import Viagem, Posicao, Estado
from modelos.motorista import Motorista
from modelos.cliente import Cliente
import math


@app.route('/tabelas/viagens', methods=['GET', 'POST'])
def get():
    if request.method == 'GET':
        return render_template('tabelas/viagens.html',
                               viagens=getViagens(),
                               estados=getEstados(),
                               mapbox_access_token=mapbox_access_token)
    elif request.method == 'POST':
        data = request.form
        estado = data.get('estado')
        cpf_motorista = data.get('cpf_motorista')
        cpf_cliente = data.get('cpf_cliente')
        motorista_id = Motorista.getMotoristaByCPF(cpf=cpf_motorista).id
        multiplicador = Motorista.query.get(
            motorista_id).serialize()['carro']['tipo_uber']['multiplicador']
        latitude_origem = data.get('posicao_origem_latitude')
        longitude_origem = data.get('posicao_origem_longitude')
        latitude_destino = data.get('posicao_destino_latitude')
        longitude_destino = data.get('posicao_destino_longitude')

        posicao_origem_json = {
            "latitude": latitude_origem,
            "longitude": longitude_origem
        }

        posicao_destino_json = {
            "latitude": latitude_destino,
            "longitude": longitude_destino
        }

        valor = calculaValor(multiplicador=multiplicador,
                             posicao_origem=posicao_origem_json,
                             posicao_destino=posicao_destino_json)
        cliente_id = Cliente.getClienteByCPF(cpf=cpf_cliente).id

        viagem = Viagem(valor=valor,
                        estado_id=estado,
                        motorista_id=motorista_id,
                        cliente_id=cliente_id)
        db.session.add(viagem)
        db.session.commit()

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


def calculaValor(multiplicador, posicao_origem, posicao_destino):
    distancia = getDistanceByCoordinates(posicao1=posicao_origem,
                                         posicao2=posicao_destino)
    return round(distancia * multiplicador, 2)


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


@app.route('/editar/viagem/<id>', methods=['GET', 'POST'])
def edit_viagem(id):
    if request.method == 'GET':
        viagem = Viagem.query.get(id)
        return render_template('tabelas/viagens.html',
                               viagens=getViagens(),
                               viagem=viagem.serialize(),
                               edit=True,
                               estados=getEstados())
    if request.method == 'POST':
        data = request.form
        if request.form['submit'] == 'fechar':
            return render_template('tabelas/viagens.html',
                                   viagens=getViagens(),
                                   edit=False,
                                   estados=getEstados())
        elif request.form['submit'] == 'editar':

            data = request.form
            viagem = Viagem.query.get(id)
            viagem.estado_id = data.get('estado')
            cpf_motorista = data.get('cpf_motorista')
            cpf_cliente = data.get('cpf_cliente')
            viagem.motorista_id = Motorista.getMotoristaByCPF(
                cpf=cpf_motorista).id
            viagem.cliente_id = Cliente.getClienteByCPF(cpf=cpf_cliente).id

            latitude_origem = data.get('posicao_origem_latitude')
            longitude_origem = data.get('posicao_origem_longitude')

            latitude_destino = data.get('posicao_destino_latitude')
            longitude_destino = data.get('posicao_destino_longitude')

            posicao_origem = viagem.getPosicaoOrigem()
            posicao_destino = viagem.getPosicaoDestino()

            posicao_origem.latitude = latitude_origem
            posicao_origem.longitude = longitude_origem

            posicao_destino.latitude = latitude_destino
            posicao_destino.longitude = longitude_destino

            db.session.commit()

            return render_template('tabelas/viagens.html',
                                   viagens=getViagens(),
                                   feedback='Viagem editado com sucesso!',
                                   edit=False,
                                   estados=getEstados())


def getDistanceByCoordinates(posicao1, posicao2):
    print(posicao1)
    lat1 = math.radians(float(posicao1['latitude']))
    lon1 = math.radians(float(posicao1['longitude']))
    print('lat1', lat1, lon1)
    lat2 = math.radians(float(posicao2['latitude']))
    lon2 = math.radians(float(posicao2['longitude']))
    print('lat2', lat2, lon2)

    dlon = lon2 - lon1
    R = 6373.0

    dlat = lat2 - lat1

    a = math.sin(
        dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    print('c', c)
    distance = R * c
    return distance