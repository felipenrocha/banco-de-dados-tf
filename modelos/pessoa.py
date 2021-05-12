from app import db


class Pessoa(db.Model):
    __tablname__ = 'pessoa'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(25), nullable=False, unique=True)
    data_nascimento = db.Column(db.Date(), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    celular = db.Column(db.String(55), nullable=False)
    sexo = db.Column(db.String(25), nullable=False)
    motoristas = db.relationship('Motorista', backref='pessoa',
                                 lazy=True)  #one to many
    clientes = db.relationship('Cliente', backref='pessoa',
                               lazy=True)  #one to many

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

    def getAll():
        pessoasQuery = Pessoa.query.all()
        pessoas = list()
        for pessoa in pessoasQuery:
            pessoas.append(pessoa.serialize())
        return pessoas

    def getPessoaByCPF(cpf):
        pessoa = Pessoa.query.filter_by(cpf=cpf).first()
        print(pessoa.serialize())
        return pessoa

    def getPessoas():
        pessoas = Pessoa.query.all()
        list_pessoas = list()
        for pessoa in pessoas:
            list_pessoas.append(pessoa.serialize())
        return list_pessoas
