from src.app.db import get_db
from src.app.data_classes.movimentacao import Movimentacao
import psycopg2.extras

def listar_movimentacoes_por_conta(id_conta: int, limite: int = 20) -> list[Movimentacao]:
    """
    Busca as últimas movimentações de uma conta.
    """
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        # Busca as movimentações mais recentes primeiro (DESC)
        query = """
            SELECT * FROM movimentacoes 
            WHERE id_conta = %s 
            ORDER BY data_hora DESC 
            LIMIT %s
        """
        cursor.execute(query, (id_conta, limite))
        resultados = cursor.fetchall()
        
        lista_movimentacoes = []
        for row in resultados:
            lista_movimentacoes.append(Movimentacao(**row))
            
        return lista_movimentacoes
    except Exception as e:
        print(f"Erro ao buscar extrato: {e}", flush=True)
        return []
    finally:
        cursor.close()