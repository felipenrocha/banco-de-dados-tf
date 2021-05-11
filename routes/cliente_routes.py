from app import app, db
from flask import request, render_template
from flask_sqlalchemy import SQLAlchemy
from modelos.cliente import CartaoDeCredito, Cliente, Pessoa


@app.route("/tabelas/clientes", methods=['GET', 'POST'])
def tabela_clientes():

    if request.method == 'GET':
        clientes = getClientes()
        return render_template('tabelas/clientes.html', clientes=clientes)
    elif request.method == 'POST':

        data = request.form
        cpf = data.get("cpf")

        try:
            pessoa = Pessoa.getPessoaByCPF(cpf)
            cliente = Cliente(pessoa_id=pessoa.id)
            db.session.add(cliente)
            db.session.commit()
            clientes = getClientes()
            return render_template('tabelas/clientes.html',
                                   feedback="Cliente adicionado com sucesso!",
                                   clientes=clientes)
        except Exception as e:
            return render_template('tabelas/clientes.html',
                                   feedback=str(e),
                                   clientes=getClientes())


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


def getClientes():
    clientesObjects = Cliente.query.all()
    clientes = list()
    for e in clientesObjects:
        clientes.append(e.serialize())
    return clientes


def getCartoes():
    cartoesObjects = CartaoDeCredito.query.all()
    cartoes = list()
    for e in cartoesObjects:
        cartoes.append(e.serialize())
    return cartoes


@app.route("/tabelas/cartoes", methods=['GET', 'POST'])
def tabela_cartoes():

    if request.method == 'GET':
        cartoes = getCartoes()
        return render_template('tabelas/cartoes.html', cartoes=cartoes)
    elif request.method == 'POST':

        data = request.form
        cpf = data.get("cpf")
        numero_cartao = data.get('numero_cartao')
        cvv = data.get('cvv')
        data_validade = data.get('data_validade')

        try:
            pessoa = Pessoa.getPessoaByCPF(cpf)
            cliente = Cliente.query.filter_by(pessoa_id=pessoa.id).first()
            cartao = CartaoDeCredito(numero=numero_cartao,
                                     cvv=cvv,
                                     data_validade=data_validade,
                                     cliente_id=cliente.id)
            db.session.add(cartao)
            db.session.commit()
            cartoes = getCartoes()
            return render_template('tabelas/cartoes.html',
                                   feedback="Cartão adicionado com sucesso!",
                                   cartoes=cartoes)
        except Exception as e:
            return render_template('tabelas/cartoes.html',
                                   feedback=str(e),
                                   cartoes=getCartoes())
