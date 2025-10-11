import mysql.connector

def criar_conexao(host: str, database: str, user: str, password: str):
    return mysql.connector.connect(
        host="localhost",
        database=database,
        user=user,
        password=password
    )

def fechar_conexao(con):
    return con.close()


