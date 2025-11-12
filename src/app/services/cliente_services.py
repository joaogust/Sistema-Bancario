from src.app.data_classes.cliente import Cliente
from src.app.db import get_db, close_db

def get_cliente(id: int):
    database = get_db()
    cursor = None

    try:
        cursor = database.cursor()
        query = "SELECT * FROM Cliente WHERE id = %s"
        cursor.execute(query, id)
        resultado = cursor.fetchone()

        if resultado is None:
            return None
        else:
            return Cliente(**resultado)

    except Exception as e:
        print("Erro ao buscar cliente: {e}")
        return None
    finally:
        if cursor:
            cursor.close()