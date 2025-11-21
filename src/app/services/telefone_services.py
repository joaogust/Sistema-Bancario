from src.app.db import get_db
from src.app.data_classes.telefone import Telefone
import psycopg2.extras

def get_telefone_by_cliente_id(id_cliente: int) -> Telefone | None:
    """
    Busca o primeiro telefone 'celular' de um cliente pelo ID do cliente.
    Retorna um objeto Telefone ou None.
    """
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        # Busca o celular como prioridade
        query = "SELECT * FROM telefones WHERE id_cliente = %s AND tipo = 'celular' LIMIT 1"
        cursor.execute(query, (id_cliente,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            # Se não achar celular, busca qualquer um
            query = "SELECT * FROM telefones WHERE id_cliente = %s LIMIT 1"
            cursor.execute(query, (id_cliente,))
            resultado = cursor.fetchone()

        if resultado is None:
            return None
        else:
            return Telefone(**resultado)
            
    except Exception as e:
        print(f"Erro ao buscar telefone: {e}", flush=True)
        return None
    finally:
        if cursor:
            cursor.close()