import psycopg2
from flask import current_app, g

def get_db():
    """
    Esse metodo cria uma conexão com o bdd ou retorna a atual.
    O 'g' vem de global, imagine ele como uma mochila temporária que o Flask dá a cada requisição que chega ao seu site.
    Ela existe apenas durante a visita daquele usuário. Quando a resposta carrega e a resposta é enviada a "mochila" (o g) é esvaziada.
    A linha "if 'db' not in g" quer dizer: "Flask, verifique se a mochila (g) dessa requisição contém um objeto etiquetado como 'db' ".

    O psycopg2 faz a conexão com o banco de dados PostgreSQL
    """
    if 'db' not in g:
        g.db = psycopg2.connect(
            host= current_app.config['POSTGRESQL_HOST'],
            dbname= current_app.config['POSTGRESQL_DATABASE'],
            user= current_app.config['POSTGRESQL_USER'],
            password= current_app.config['POSTGRESQL_PASSWORD']
        )
    return g.db

def close_db(e=None):
    """
    O comando "db = g.pop('db', None)" verifica tem uma conexão na "mochila" e, se tiver, tira ela e armazena em db.
    Se houver alguma conexão ela é fechada.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
