from src.app.data_classes.ted import Ted
from src.app.db import get_db, close_db

def create_ted(id: int, num_conta_destino: int, agencia_destino: int, tipo_conta_destino: str, instituicao_destino: str, nome_destino: str, cpf_cnpj_destino: int):
    database = get_db()
    cursor = database.cursor()
    query = "INSERT INTO Ted (id, num_conta_destino, agencia_destino, tipo_conta_destino, instituicao_destino, nome_destino, cpf_cnpj_destino) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (id, num_conta_destino, agencia_destino, tipo_conta_destino, instituicao_destino, nome_destino, cpf_cnpj_destino))
    database.commit()
    close_db(database)

def get_ted(id: int):
    database = get_db()
    cursor = database.cursor()
    query = "SELECT * FROM Ted WHERE id = ?"
    resultado = cursor.execute(query, id)
    if resultado is None:
        return None
    else:
        return Ted(**resultado)