from src.app.data_classes.conta import Conta
from src.app.db import get_db, close_db
from datetime import date

def create_conta(id: int, tipo: str, numero: int, saldo: float, data_hora_abertura: date, data_hora_fechamento: date, estado: str, id_cliente: int):
    database = get_db()
    cursor = database.cursor()
    query = "INSERT INTO Conta (id, tipo, numero, saldo, data_hora_abertura, data_hora_fechamento, estado, id_cliente) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (id, tipo, numero, saldo, data_hora_abertura, data_hora_fechamento, estado, id_cliente))
    database.commit()
    close_db(database)

def get_conta(id: int):
    database = get_db()
    cursor = database.cursor()
    query = "SELECT * FROM Conta WHERE id = ?"
    resultado = cursor.execute(query, id)
    if resultado is None:
        return None
    else:
        return Conta(**resultado)