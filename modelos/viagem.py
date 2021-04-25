from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from modelos.motorista import Motorista
from modelos.cliente import Cliente

class Viagem(db.Model):
    __tablename__ = 'viagem'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    _estado = relationship("Estado", back_populates="relationships")

    motorista_id = Column(Integer, ForeignKey('motorista.id'))  # one to one
    _motorista = relationship("Motorista", back_populates="relationshipViagem")

    cliente_id = Column(Integer, ForeignKey('cliente.id'))  # one to one
    _cliente = relationship("Cliente", back_populates="relationshipViagem")

    _posicao = relationship("Posicao",
                            back_populates="_posicao")  # one to many posicao

    def __init__(self, valor, estado_id, motorista_id, cliente_id):
        self.valor = valor
        self.estado_id = estado_id
        self.motorista_id = motorista_id
        self.cliente_id = cliente_id
    def serialize(self):
        return {
            'id': self.id,
            'valor':self.valor,
            'estado': Estado.query.get(self.estado_id).descricao,
            'motorista': Motorista.query.get(self.motorista_id).nome,
            'cliente': Cliente.query.get(self.cliente_id).nome
        }
    def getAll():
        return Viagem.query.all()



# One (Viagem) to Many (Posicao)


class Posicao(db.Model):
    __tablename__ = 'posicao'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    viagem_id = Column(Integer, ForeignKey('viagem.id'))
    _posicao = relationship("Viagem", back_populates="_posicao")

    def __init__(self, tipo, latitude, longitude, viagem_id):
        self.latitude = latitude
        self.longitude = longitude
        self.tipo = tipo
        self.viagem_id = viagem_id

    def serialize(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude
        }


class Estado(db.Model):
    __tablename__ = 'estado'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    descricao = Column(db.String(35), nullable=False)

    relationships = relationship("Viagem", back_populates="_estado")

    def __init__(self, descricao):
        self.descricao = descricao
    def getAll():
        estadosQuery = Estado.query.all()
        estados = list()
        for estado in estadosQuery:
            estados.append(estado.serialize())
        return estados
    def serialize(self):
        return {
            'id': self.id,
            'descricao': self.descricao
        }
