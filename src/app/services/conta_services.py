from src.app.db import get_db
from src.app.data_classes.conta import Conta
import psycopg2.extras

def get_conta_by_cliente_id(id_cliente: int) -> Conta | None:
    """
    Busca a primeira conta 'ativa' de um cliente pelo ID do cliente.
    Retorna um objeto Conta ou None.
    (Corrigido para PostgreSQL e para usar RealDictCursor)
    """
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        query = """
            SELECT * FROM contas 
            WHERE id_cliente = %s AND estado = 'ativa' 
            LIMIT 1
        """
        cursor.execute(query, (id_cliente,))
        
        resultado = cursor.fetchone()
        
        if resultado is None:
            return None
        else:
            return Conta(**resultado)
            
    except Exception as e:
        print(f"Erro ao buscar conta: {e}", flush=True)
        return None
    finally:
        if cursor:
            cursor.close()