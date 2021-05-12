from app import db
from modelos.viagem import MetodoPagamento


def metodosPagamentoSeed():
    if len(MetodoPagamento.getAll()) == 0:
        tipos = [{
            "nome": "Dinheiro"
        }, {
            "nome": "Cartão de Crédito"
        }, {
            "nome": "Uber Cŕedits"
        }, 
        {
            "nome": "Promocional"
        },
        {
            "nome": "Pix"
        }
        ]

        for tipo in tipos:
            print(tipo)
            tipo = MetodoPagamento(tipo['nome'])
            db.session.add(tipo)
            db.session.commit()
