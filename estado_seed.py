from app import db
from modelos.viagem import Estado


def seed():
    if len(Estado.getAll()) == 0:
        tipos = [{
            "descricao": "ESPERANDO CLIENTE NO LOCAL",
        }, {
            "descricao": "LOCALIZANDO MOTORISTA",
        }, {
            "descricao": "EM VIAGEM",
        }, {
            "descricao": "CONCLUÍDA",
        }, {
            "descricao": "NÃO FINALIZADA",
        }]

        for tipo in tipos:
            print(tipo)
            tipo = Estado(tipo['descricao'])
            db.session.add(tipo)
            db.session.commit()


seed()
