from app import db

class Posicao(db.Model):
    __tablename__ = 'posicao'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    relationshipsOrigem = db.relationship("Viagem", back_populates="_origem")
    relationshipDestino = db.relationship("Viagem", back_populates="_destino")


    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def serialize(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
