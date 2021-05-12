import json
from app import db
from modelos.pessoa import Pessoa

with open('seeds/pessoas.json') as pessoas:
    data = json.load(pessoas)


def pessoasSeed():
    if len(Pessoa.getAll()) == 0:
        for pessoa in data:
            pessoa_db = Pessoa(
                nome=pessoa['nome'],
                cpf=pessoa['cpf'],
                data_nascimento=pessoa['data_nasc'],
                celular=pessoa['celular'],
                email=pessoa['email'],
                sexo=pessoa['sexo'])
            db.session.add(pessoa_db)
            db.session.commit()
            print(pessoa_db.serialize())
        
pessoasSeed()