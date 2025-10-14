from src.app.data_classes.cliente import Cliente
from src.app.db import get_db, close_db
from datetime import date
from decimal import Decimal

def create_cliente(id: int, rg: int, cpf: int, nome: str, data_nasc: date, email: str, salario: Decimal, vl_patrimonio: Decimal, id_profissao: int):
    database = get_db()
    cursor = database.cursor()
    query = "INSERT INTO Cliente (id, rg, cpf, nome, data_nasc, email, salario, vl_patrimonio, id_profissao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (id, rg, cpf, nome, data_nasc, email, salario, vl_patrimonio, id_profissao))
    database.commit()
    close_db(database)

def get_cliente(id: int):
    database = get_db()
    cursor = database.cursor()
    query = "SELECT * FROM Cliente WHERE id = ?"
    resultado = cursor.execute(query, id)
    if resultado is None:
        return None
    else:
        return Cliente(**resultado)