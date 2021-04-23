from app import db

from modelos.carro import Carro


class Motorista(db.Model):
    __tablname__ = 'motorista'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    nome = db.Column(db.String(25))
    cpf = db.Column(db.String(25), nullable=False, unique=True)
    data_nascimento = db.Column(db.Date(), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    celular = db.Column(db.String(25), nullable=False)
    sexo = db.Column(db.String(25), nullable=False)
    carro_id = db.Column(db.Integer, db.ForeignKey('carro.id'), nullable=False)
    _carro = db.relationship("Carro", back_populates="relationships")

    relationshipMotorista = db.relationship("Viagem", back_populates="_motorista")

    def __init__(self, nome, cpf, data_nascimento, celular, email, sexo,
                 carro_id):
        print(email)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.celular = celular
        self.email = email
        self.sexo = sexo
        self.carro_id = carro_id

    def __repr__(self):
        return '<id{}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento,
            'celular': self.celular,
            'sexo': self.sexo,
            'carro': self.getCarroById()
        }
    def getCarroById(self):
        carro = Carro.query.get(self.carro_id)
        print('carroid', carro.id)
        return {
            "placa": carro.placa,
            "modelo": carro.modelo
        }
