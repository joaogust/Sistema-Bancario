from src.app.data_classes.endereco import Endereco
from src.app.db import get_db, close_db

def create_endereco(id: int, complemento: str, rua: str, numero: str, cidade: str, estado: str, pais: str, cep: str):
    database = get_db()
    cursor = database.cursor()
    query = "INSERT INTO Endereco (id, complemento, rua, numero, cidade, estado, pais, cep) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (id, complemento, rua, numero, cidade, estado, pais, cep))
    database.commit()
    close_db(database)

def get_endereco(id: int):
    database = get_db()
    cursor = database.cursor()
    query = "SELECT * FROM Endereco WHERE id = ?"
    resultado = cursor.execute(query, id)
    if resultado is None:
        return None
    else:
        return Endereco(**resultado)