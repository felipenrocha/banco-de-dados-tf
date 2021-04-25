from app import db


class Cliente(db.Model):
    __tablname__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    nome = db.Column(db.String(25))
    cpf = db.Column(db.String(25), nullable=False, unique=True)
    data_nascimento = db.Column(db.Date(), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    celular = db.Column(db.String(25), nullable=False)
    sexo = db.Column(db.String(25), nullable=False)


    
    relationshipViagem = db.relationship("Viagem", back_populates="_cliente")




    def __init__(self, nome, cpf, data_nascimento, celular, email, sexo):
        print(email)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.celular = celular
        self.email = email
        self.sexo = sexo

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
        }
    def getClienteByCPF(cpf):
        cliente = Cliente.query.filter_by(cpf=cpf).first()
        return cliente
