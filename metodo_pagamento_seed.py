from app import db
from modelos.viagem import MetodoPagamento


def seed():
    if len(MetodoPagamento.getAll()) == 0:
        tipos = [{
            "nome": "Dinheiro"
        }, {
            "nome": "Cartão de Crédito"
        }]

        for tipo in tipos:
            print(tipo)
            tipo = MetodoPagamento(tipo['nome'])
            db.session.add(tipo)
            db.session.commit()


seed()
