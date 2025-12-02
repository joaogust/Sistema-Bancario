from src.app.db import get_db
from src.app.data_classes.movimentacao import Movimentacao
import psycopg2.extras
from decimal import Decimal

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
    
def realizar_saque_db(id_conta: int, valor: Decimal):
    """
    Chama a PROCEDURE SQL 'realizar_saque' no banco para sacar o valor.
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Chama a função SQL (PROCEDURE) definida no schema
        # A procedure lida com a verificação de saldo e o registro da movimentação
        query = "SELECT realizar_saque(%s, %s)"
        cursor.execute(query, (id_conta, valor))
        db.commit()
        return True
        
    except psycopg2.Error as e:
        db.rollback()
        # O PostgreSQL armazena a exceção da procedure no objeto de erro.
        # Tentamos extrair a mensagem de erro específica (ex: 'Saldo insuficiente')
        error_message = str(e)
        if "Saldo insuficiente" in error_message:
            raise ValueError("Saldo insuficiente para o saque.")
        if "Conta não encontrada" in error_message:
            raise ValueError("Conta não encontrada.")
            
        print(f"Erro no SQL ao realizar saque: {e}", flush=True)
        raise
    except Exception as e:
        db.rollback()
        print(f"Erro inesperado ao realizar saque: {e}", flush=True)
        raise
    finally:
        cursor.close()