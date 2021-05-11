from app import db
from modelos.pessoa import Pessoa


class Cliente(db.Model):
    __tablname__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    pessoa_id = db.Column(db.Integer,
                          db.ForeignKey('pessoa.id'),
                          nullable=False,
                          unique=True)  # many to one

    relationshipViagem = db.relationship('Viagem',
                                         backref='Cliente',
                                         lazy=True)

    def __init__(self, pessoa_id):
        self.pessoa_id = pessoa_id

    def __repr__(self):
        return '<id{}>'.format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            'informacoes_pessoais': self.getPessoaById().serialize(),
            'cartoes': self.getCartoes()
        }

    def getClienteByCPF(cpf):
        cliente = Cliente.query.filter_by(cpf=cpf).first()
        return cliente

    def getPessoaById(self):
        return Pessoa.query.get(self.pessoa_id)

    def getCartoes(self):
        cartoes = CartaoDeCredito.query.filter_by(cliente_id=self.id)
        list_cartoes = list()
        for cartao in cartoes:
            list_cartoes.append(cartao.serialize())
        return cartoes


class CartaoDeCredito(db.Model):
    __tablname__ = 'cartao_de_credito'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    numero = db.Column(db.String(25), nullable=False, unique=True)
    cvv = db.Column(db.Integer, nullable=False)
    data_validade = db.Column(db.String(25), nullable=False)
    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey('cliente.id'),
        nullable=False,
    )  # many to one

    metodos = db.relationship('MetodoPagamento',
                              backref='cartao_de_credito',
                              lazy=True)  #one to many

    def __init__(self, numero, cvv, data_validade, cliente_id):
        self.numero = numero
        self.cvv = cvv
        self.data_validade = data_validade
        self.cliente_id = cliente_id

    def serialize(self):
        return {
            'id':self.id, 
            'proprietario': {
                'nome': self.getProprietario()['nome'],
                'cpf': self.getProprietario()['cpf']
            },
            'info': {
                'numero': self.encode_card_number(),
                'cvv': self.cvv,
                'data_validade': self.data_validade
            }
        }

    def encode_card_number(self):
        return '****-****-****-' + self.numero[-4:]

    def getProprietario(self):
        cliente = Cliente.query.get(self.cliente_id)
        pessoa = Pessoa.query.get(cliente.pessoa_id)
        return pessoa.serialize()