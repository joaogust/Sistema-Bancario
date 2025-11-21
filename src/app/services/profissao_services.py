from src.app.data_classes.profissao import Profissao
from src.app.db import get_db
import psycopg2.extras # NECESSÁRIO PARA RETORNAR DICIONÁRIOS

def listar_profissoes():
    """
    Busca todas as profissões no banco de dados, ordenadas por nome.
    Retorna uma lista de dicionários.
    """
    db = get_db()
    # Usar RealDictCursor faz o banco retornar dicionários (ex: {'id': 1, 'nome': 'Advogado'})
    # Isso é perfeito para usar no template Jinja2 (ex: p.id, p.nome)
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Usamos 'profissoes' (minúsculo) como é o padrão SQL.
    # Se sua tabela foi criada com "Profissao" (maiúsculo), 
    # você deve usar: 'SELECT id, nome FROM "Profissao" ORDER BY nome ASC'
    query = "SELECT id, nome FROM profissoes ORDER BY nome ASC"
    
    try:
        cursor.execute(query)
        profissoes = cursor.fetchall()
        return profissoes
    except Exception as e:
        print(f"Erro ao buscar profissões: {e}")
        return [] # Retorna lista vazia em caso de erro
    finally:
        cursor.close()

def get_profissao(id: int):
    """
    Busca uma profissão específica pelo ID.
    """
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # 1. Use %s em vez de ?
    # 2. Use 'profissoes' (ou "Profissao" se você forçou o nome)
    query = 'SELECT * FROM profissoes WHERE id = %s'
    
    try:
        # 3. O segundo argumento DEVE ser uma tupla (por isso o (id,))
        cursor.execute(query, (id,))
        
        # 4. 'execute' não retorna nada, 'fetchone' é quem busca o dado
        resultado = cursor.fetchone()
        
        if resultado:
            # Assumindo que sua data class 'Profissao' aceita um dicionário
            return Profissao(**resultado)
        else:
            return None
    finally:
        cursor.close()

def create_profissao(id: int, nome: str):
    """
    Cria uma nova profissão. (Corrigido)
    """
    db = get_db()
    cursor = db.cursor()
    
    # 1. Use %s em vez de ?
    query = "INSERT INTO profissoes (id, nome) VALUES (%s, %s)"
    
    try:
        cursor.execute(query, (id, nome))
        db.commit() # Salva as mudanças no banco
    except Exception as e:
        db.rollback() # Desfaz em caso de erro
        print(f"Erro ao criar profissão: {e}")
    finally:
        cursor.close()

# NOTA: Removi a chamada 'close_db(database)' de dentro das funções.
# O seu arquivo 'db.py' deve ser responsável por fechar a conexão
# automaticamente no final de cada request (usando app.teardown_appcontext).