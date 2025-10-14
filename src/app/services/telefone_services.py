from src.app.data_classes.telefone import Telefone
from src.app.db import get_db, close_db

def create_telefone(id: int, numero: int, tipo: str, id_cliente: int):
    database = get_db()
    cursor = database.cursor()
    query = "INSERT INTO Telefone (id, numero, tipo, id_cliente) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (id, numero, tipo, id_cliente))
    database.commit()
    close_db(database)

def get_telefone(id: int):
    database = get_db()
    cursor = database.cursor()
    query = "SELECT * FROM Telefone WHERE id = ?"
    resultado = cursor.execute(query, id)
    if resultado is None:
        return None
    else:
        return Telefone(**resultado)