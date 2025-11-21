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
    # RealDictCursor faz o banco retornar dicionários (ex: {'id': 1, 'saldo': ...})
    # Isso é essencial para 'Conta(**resultado)' funcionar.
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        # 1. Query na tabela 'contas' (minúsculo)
        # 2. Usa %s em vez de ?
        query = """
            SELECT * FROM contas 
            WHERE id_cliente = %s AND estado = 'ativa' 
            LIMIT 1
        """
        # 3. Passa os parâmetros como uma tupla
        cursor.execute(query, (id_cliente,))
        
        # 4. Busca o resultado com fetchone()
        resultado = cursor.fetchone()
        
        if resultado is None:
            return None
        else:
            # 5. Agora 'resultado' é um dicionário, então Conta(**resultado) funciona
            return Conta(**resultado)
            
    except Exception as e:
        print(f"Erro ao buscar conta: {e}", flush=True)
        return None
    finally:
        if cursor:
            cursor.close()

# NOTA: As funções 'create_conta' e 'get_conta' (pelo id da conta)
# não são necessárias para o fluxo de cadastro e login no momento.
# A função 'criar_cliente_completo' (em cliente_services.py)
# já está cuidando da criação da conta.