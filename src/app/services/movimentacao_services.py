from src.app.data_classes.movimentacao import Movimentacao
from src.app.db import get_db, close_db
from datetime import datetime

def create_movimentacao(id: int, id_conta: int, data_hora: datetime, valor: float, tipo: str, id_pix: int, id_ted: int):
    database = get_db()
    cursor = database.cursor()
    query = "INSERT INTO Movimentacao (id, id_conta, data_hora, valor, tipo, id_pix, id_ted) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (id, id_conta, data_hora, valor, tipo, id_pix, id_ted))
    database.commit()
    close_db(database)

def get_movimentacao(id: int):
    database = get_db()
    cursor = database.cursor()
    query = "SELECT * FROM Movimentacao WHERE id = ?"
    resultado = cursor.execute(query, id)
    if resultado is None:
        return None
    else:
        return Movimentacao(**resultado)