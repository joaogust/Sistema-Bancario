from src.app.data_classes.cliente import Cliente
from src.app.db import get_db, close_db
from werkzeug.security import check_password_hash # Para verificar a senha

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

def verificar_cpf_existente(cpf: str) -> bool:
    """
    Verifica se um CPF já existe na tabela de clientes.
    Retorna True se existir, False se não.
    """
    
    # 1. Obter uma conexão com o banco
    database = get_db()
    
    # 2. Definir a consulta SQL
    # Usamos "SELECT 1" por ser leve. Só queremos saber se "algo" existe.
    query = "SELECT 1 FROM cliente WHERE cpf = %s LIMIT 1"
    
    # 3. Executar a consulta
    cursor = database.cursor()
    cursor.execute(query, (cpf,))
    
    # 4. Analisar o resultado
    resultado = cursor.fetchone()
    cursor.close()
    
    # 5. Retornar a resposta
    if resultado:
        return True  # O CPF foi encontrado
    else:
        return False # O CPF está livre

def validar_login(cpf_sujo: str, senha_texto_plano: str):
    """
    Valida o login de um cliente.
    Retorna o objeto Cliente se for válido, None se for inválido.
    """
    if not cpf_sujo or not senha_texto_plano:
        return None

    # 1. Limpar o CPF para consultar o banco
    cpf_limpo = cpf_sujo.replace('.', '').replace('-', '')

    database = get_db()
    # Usar dictionary=True facilita transformar os dados em um objeto
    cursor = database.cursor(dictionary=True) 

    try:
        # 2. Buscar o cliente pelo CPF limpo
        # IMPORTANTE: Selecione a senha hasheada (ex: 'senha_hash')
        query = "SELECT id_cliente, nome, cpf, senha_hash FROM cliente WHERE cpf = %s"
        cursor.execute(query, (cpf_limpo,))
        dados_cliente = cursor.fetchone()

        if not dados_cliente:
            return None # Cliente não encontrado

        # 3. Verificar se a senha bate
        senha_hash_do_banco = dados_cliente['senha_hash']
        
        # A função check_password_hash compara a senha do formulário
        # com o hash armazenado no banco de dados.
        if check_password_hash(senha_hash_do_banco, senha_texto_plano):
            # Senha correta!
            # (Vamos assumir que sua classe Cliente aceita esses kwargs)
            cliente = Cliente(**dados_cliente) 
            return cliente
        else:
            # Senha incorreta
            return None

    except Exception as e:
        print(f"Erro ao validar login: {e}")
        return None
    finally:
        cursor.close()