# Projeto final de Banco de Dados: SGBD p/ Sistemas Prestadora de Serviços Eletrônicos na Área do Transporte Privado Urbano 

Modelo Entidade Relacional: 

![alt text](https://github.com/felipenrocha/[reponame]/banco-de-dados-tf.git/master/mer.png?raw=true)

# Instalation Process

## Pré-requisitos


## Por onde eu começo?

Existem algumas formas de você configurar o seu ambiente. Nesta seção iremos apresentar apenas uma das formas possíveis.

* 1. O primeiro passo é fazer o checkout do seu código. Utilizando um terminal, faça um clone do repositório.

```
git clone https://gitlab.com/felipenrocha19/banco-de-dados-tf.git
```
* 2. Criação de um ambiente virtual:

```
python3 -m venv banco-de-dados-tf/env
```

* 3. Entre no repositório

```
cd banco-de-dados-tf
```

* 4. O próximo passo é ativar o terminal e carregar as configurações python.

```
source env/bin/activate
```

* 5. Agora você precisa instalar as bibliotecas utilizadas pela ferramenta Flask e SQLAlchemy.
```
pip3 install -r requirements.txt
```

* 6. Criando o Banco de Dados: (Estou utilizando o nome de uber_db p/ facilitar no desenvolvimento)

É necessário o Sistema PostgreSQL e que já possua um usuário:

P/ Linux:
```
sudo -u name_of_user createdb uber_db
```
P/ checar o banco de dados pelo terminal:
```

psql -U name_of_user -d uber_db
```


* 7. O último passo é exportar as váriaveis de ambiente necessárias p/ o deploy. Como esse é um trabalho de cunho puramente educativo, estou setando sempre para modo de desenvolvimento:

Comando no Linux:

```
export APP_SETTINGS="config.DevelopmentConfig"

export DATABASE_URL="postgresql:///uber_db"
```

Comando no Windows:

```
set APP_SETTINGS="config.DevelopmentConfig"

set DATABASE_URL="postgresql:///uber_db"
```


Pronto! Para testar o código, basta executar:

Inicializar op Banco de dados criando as tabelas:
```
python manage.py db init
python manage.py db migrate
python manager.py db upgrade
```

```
python manage.py runserver

```

* Comandos adicionais:

Migrate:
```
python manage.py db init
python manage.py db migrate
python manager.py db upgrade

```

Seed (Tabelas: Tipo Uber, Métodos Pagamento e Estados da Viagem):

```
python tipo_uber_seed.py
python metodo_pagamento_seed.py
python estado_seed.py

```



