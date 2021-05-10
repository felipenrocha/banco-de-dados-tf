from app import db

from modelos.carro import Carro
from modelos.pessoa import Pessoa


class Motorista(db.Model):
    __tablname__ = 'motorista'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)


    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'),
        nullable=False) # many to one

    carros = db.relationship('Carro', backref='Motorista', lazy=True) # one to many 

    relationshipViagem = db.relationship("Viagem", backref='Motorista', lazy=True) # one to many


    def __init__(self, pessoa_id):
        self.pessoa_id = pessoa_id


    def __repr__(self):
        return '<id{}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'informacoes_pessoais': self.getPessoaById().serialize(),
            'carro(s)': self.getCarroById()
        }

    
    def getPessoaById(self):
        return Pessoa.query.get(self.pessoa_id)


    def getCarroById(self):
        carros = Carro.query.filter_by(motorista_id=self.id)
        list_carros = list()
        for carro in carros:
            list_carros.append(carro.serialize())
        return list_carros


    def getMotoristaByCPF(cpf):
        pessoa = Pessoa.getPessoaByCPF(cpf=cpf)
        motorista = Motorista.query.filter_by(pessoa_id=pessoa.id).first()
        print(motorista.serialize())
        return motorista