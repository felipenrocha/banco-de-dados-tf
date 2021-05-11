from app import db
from modelos.viagem import MetodoPagamento


def seed():
    if len(MetodoPagamento.getAll()) == 0: 
        tipos = [{
            "nome": "UberX",
            "multiplicador": 0.8
        }, {
            "nome": "Comfort",
            "multiplicador": 1
        }, {
            "nome": "Black",
            "multiplicador": 1.5
        }, {
            "nome": "UberBAG",
            "multiplicador": 1.5
        }]

        for tipo in tipos:
            print(tipo)
            tipo = TipoUber(tipo['nome'], tipo['multiplicador'])
            db.session.add(tipo)
            db.session.commit()


seed()
