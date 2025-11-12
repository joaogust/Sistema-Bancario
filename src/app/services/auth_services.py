from src.app.data_classes.cliente import Cliente
from src.app.db import get_db
from datetime import date
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash

def create_cliente(rg: int, cpf: int, nome: str, data_nasc: date, email: str, salario: Decimal, vl_patrimonio: Decimal, id_profissao: int, senha: str):
    database = get_db()
    cursor = None
    senha_hash = generate_password_hash(senha)

    try:
        cursor = database.cursor()
        query = ("INSERT INTO Cliente (rg, cpf, nome, data_nasc, email, salario, vl_patrimonio, id_profissao, senha_hash) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                 "RETURNING id_cliente")
        cursor.execute(query, (rg, cpf, nome, data_nasc, email, salario, vl_patrimonio, id_profissao, senha_hash))
        new_id = cursor.fetchone()[0]

        database.commit()
        return new_id

    except Exception as e:
        if database:
            database.rollback()
        print("Erro ao criar cliente: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

def validar_login(cpf: str, senha: str):
    database = get_db()
    cursor = None

    try:
        cursor = database.cursor()
        query = ("SELECT id_cliente FROM Cliente WHERE cpf = %s")
        cursor.execute(query, (cpf))

        resultado = cursor.fetchone()

        if resultado is None:
            return None

        senha_hash = resultado['senha_hash']

        if check_password_hash(senha_hash, senha):
            return Cliente(**resultado)
        else:
            return None

    except Exception as e:
        print("Erro ao validar login: {e}")
        return None
    finally:
        if cursor:
            cursor.close()