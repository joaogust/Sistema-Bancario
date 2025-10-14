from src.app.data_classes.profissao import Profissao
from src.app.db import get_db, close_db

def create_profissao(id: int, nome: str):
    database = get_db()
    cursor = database.cursor()
    query = "INSERT INTO Profissao (id, nome) VALUES (?, ?)"
    cursor.execute(query, (id, nome))
    database.commit()
    close_db(database)

def get_profissao(id: int):
    database = get_db()
    cursor = database.cursor()
    query = "SELECT * FROM Profissao WHERE id = ?"
    resultado = cursor.execute(query, id)
    if resultado is None:
        return None
    else:
        return Profissao(**resultado)