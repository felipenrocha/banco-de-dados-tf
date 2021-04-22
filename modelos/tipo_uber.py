from app import db

class TipoUber(db.Model):
    __tablname__ = 'tipo_uber'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    multiplicador = db.Column(db.Float())
    relationships = db.relationship("Carro", back_populates="_tipo_uber")
    def __init__(self, nome, multiplicador):
        self.nome = nome
        self.multiplicador = multiplicador
    
    def __repr__(self):
        return '<id{}>'.format(self.id)
    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'multiplicador': self.multiplicador,
        }
    def getAll():
        tiposQuery = TipoUber.query.all()
        tipos = list()
        for tipo in tiposQuery:
            tipos.append(tipo.serialize())
        print(tipos)
        return tipos