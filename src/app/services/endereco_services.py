from src.app.db import get_db
from src.app.data_classes.endereco import Endereco
import psycopg2.extras

def get_endereco_by_cliente_id(id_cliente: int) -> Endereco | None:
    """
    Busca o primeiro endereço de um cliente pelo ID do cliente.
    Retorna um objeto Endereco ou None.
    """
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        query = "SELECT * FROM enderecos WHERE id_cliente = %s LIMIT 1"
        cursor.execute(query, (id_cliente,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            return None
        else:
            return Endereco(**resultado)
            
    except Exception as e:
        print(f"Erro ao buscar endereço: {e}", flush=True)
        return None
    finally:
        if cursor:
            cursor.close()