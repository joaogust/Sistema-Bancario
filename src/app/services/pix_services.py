from src.app.data_classes.pix import Pix
from src.app.db import get_db, close_db

def create_pix(id: int, tipo_chave: str, chave_destino: str):
    database = get_db()
    cursor = database.cursor()
    query = "INSERT INTO Pix (id, tipo_chave, chave_destino) VALUES (?, ?, ?)"
    cursor.execute(query, (id, tipo_chave, chave_destino))
    database.commit()
    close_db(database)

def get_pix(id: int):
    database = get_db()
    cursor = database.cursor()
    query = "SELECT * FROM Pix WHERE id = ?"
    resultado = cursor.execute(query, id)
    if resultado is None:
        return None
    else:
        return Pix(**resultado)