from src.app.db import get_db
from src.app.data_classes.chave_pix import ChavePix
import psycopg2.extras
import random
import uuid

def listar_chaves_por_conta(id_conta: int) -> list[ChavePix]:
    """
    Busca todas as chaves PIX associadas a uma conta.
    """
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        query = "SELECT * FROM chaves_pix WHERE id_conta = %s"
        cursor.execute(query, (id_conta,))
        resultados = cursor.fetchall()
        
        lista_chaves = []
        for row in resultados:
            lista_chaves.append(ChavePix(**row))
            
        return lista_chaves
    except Exception as e:
        print(f"Erro ao buscar chaves PIX: {e}", flush=True)
        return []
    finally:
        cursor.close()

def criar_chave_pix(id_conta: int, tipo_chave: str, valor_chave: str | None = None):
    """
    Cria uma nova chave PIX para a conta.
    Se o tipo for 'aleatoria', gera um UUID.
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        chave_final = valor_chave
        
        # Se for aleatória, gera um UUID
        if tipo_chave == 'aleatoria':
            chave_final = str(uuid.uuid4())
            
        # Validação básica (você pode melhorar isso)
        if not chave_final:
            raise ValueError("O valor da chave não pode ser vazio.")

        query = """
            INSERT INTO chaves_pix (chave, tipo, id_conta)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (chave_final, tipo_chave, id_conta))
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar chave PIX: {e}", flush=True)
        raise e # Re-lança para a rota tratar
    finally:
        cursor.close()

def excluir_chave_pix(id_chave: int, id_conta: int):
    """
    Exclui uma chave PIX específica.
    Verifica se a chave pertence à conta correta antes de excluir.
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # A exclusão é feita apenas se o id_chave e o id_conta (do usuário logado) baterem.
        query = "DELETE FROM chaves_pix WHERE id = %s AND id_conta = %s"
        cursor.execute(query, (id_chave, id_conta))
        
        if cursor.rowcount == 0:
            raise ValueError("Chave não encontrada ou não pertence à sua conta.")
            
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()
        # Se for uma chave obrigatória (CPF, por exemplo), pode haver um erro de integridade (FK)
        print(f"Erro ao excluir chave PIX: {e}", flush=True)
        raise e
    finally:
        cursor.close()