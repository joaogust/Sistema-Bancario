from src.app.data_classes.chave_pix import Chave_pix
from src.app.db import get_db, close_db

def create_chave_pix(id: int, chave: str, tipo: str, id_conta: int):
    database = get_db()
    cursor = database.cursor()
    query = "INSERT INTO Chave_pix (id, chave, tipo, id_conta) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (id, tipo, chave, id_conta))
    database.commit()
    close_db(database)

def get_chave_pix(id: int):
    database = get_db()
    cursor = database.cursor()
    query = "SELECT * FROM Chave_pix WHERE id = ?"
    resultado = cursor.execute(query, id)
    if resultado is None:
        return None
    else:
        return Chave_pix(**resultado)