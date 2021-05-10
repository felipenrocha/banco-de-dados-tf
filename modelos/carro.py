from app import db

from modelos.tipo_uber import TipoUber


class Carro(db.Model):
    __tablname__ = 'carro'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    modelo = db.Column(db.String(25))
    chassi = db.Column(db.String(25), nullable=False)
    marca = db.Column(db.String(25), nullable=False)
    placa = db.Column(db.String(25), nullable=False, unique=True)
    ano = db.Column(db.String(25), nullable=False)
    cor = db.Column(db.String(25), nullable=False)
    
    
    tipo_uber_id = db.Column(db.Integer, db.ForeignKey('tipo_uber.id'), nullable=False) # many to one
    motorista_id = db.Column(db.Integer, db.ForeignKey('motorista.id'), nullable=False)


    def __init__(self, modelo, chassi, marca, ano, placa, cor, tipo_uber_id, motorista_id):
        print(placa)
        self.modelo = modelo
        self.chassi = chassi
        self.marca = marca
        self.ano = ano
        self.placa = placa
        self.cor = cor
        self.tipo_uber_id = tipo_uber_id
        self.motorista_id  = motorista_id

    def __repr__(self):
        return '<id{}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'modelo': self.modelo,
            'placa': self.placa,
            'chassi': self.chassi,
            'marca': self.marca,
            'ano': self.ano,
            'cor': self.cor,
            'tipo_uber': self.getTipo()
        }

    def getTipo(self):
        tipoQuery = TipoUber.query.get(self.tipo_uber_id)
        return {
            "nome": tipoQuery.nome,
            "multiplicador": tipoQuery.multiplicador,
        }
