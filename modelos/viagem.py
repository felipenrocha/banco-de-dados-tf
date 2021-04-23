from app import db

class Viagem(db.Model):
    __tablename__ = 'viagem'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    origem_id = db.Column(db.Integer, db.ForeignKey('posicao.id'), nullable=False)
    destino_id = db.Column(db.Integer, db.ForeignKey('posicao.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    motorista_id = db.Column(db.Integer, db.ForeignKey('motorista.id'), nullable=False)


 # TODO: ORIGEM, DESTINO MANY TO MANY RELATIONSHIPS
    _origem = db.relationship("Posicao", back_populates="relationshipsOrigem")
    _destino = db.relationship("Posicao", back_populates="relationshipDestino")
    _cliente =  db.relationship("Cliente", back_populates="relationshipCliente")
    _motorista =  db.relationship("Motorista", back_populates="relationshipMotorista")

    def __init__(self, latitude, longitude, origem, destino):
        self.latitude = latitude
        self.longitude = longitude
        self.origem_id = origem
        self.destino_id = destino

    def serialize(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }
