from src.app.data_classes.cliente import Cliente
from src.app.db import get_db
import psycopg2.extras # Para usar RealDictCursor
import random
from werkzeug.security import generate_password_hash, check_password_hash

# --- Funções para Login e Busca (Corrigidas) ---

def get_cliente(id: int):
    """
    Busca um cliente específico pelo ID.
    Retorna um objeto Cliente ou None. (Corrigido para psycopg2)
    """
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        query = "SELECT * FROM clientes WHERE id = %s"
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()
        if resultado is None:
            return None
        else:
            return Cliente(**resultado)
    except Exception as e:
        print(f"Erro ao buscar cliente: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

def validar_login(cpf_sujo: str, senha_texto_plano: str):
    """
    Valida o login de um cliente.
    Retorna o objeto Cliente se for válido, None se for inválido.
    (Corrigido para psycopg2 e schema)
    """
    if not cpf_sujo or not senha_texto_plano:
            return "CPF ou senha não fornecidos."

    cpf_limpo = cpf_sujo.replace('.', '').replace('-', '')
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) 

    try:
        # Coluna 'id' da tabela 'clientes'
        query = "SELECT id, nome, cpf, senha_hash FROM clientes WHERE cpf = %s"
        cursor.execute(query, (cpf_limpo,))
        dados_cliente = cursor.fetchone()

        if not dados_cliente:
            print(f"Login falhou: CPF {cpf_limpo} não encontrado.")
            return f"Login falhou: CPF {cpf_limpo} não encontrado."

        senha_hash_do_banco = dados_cliente['senha_hash']
        
        if check_password_hash(senha_hash_do_banco, senha_texto_plano):
            # Senha correta!
            # Assumindo que a classe Cliente tenha 'id' e 'nome'
            class ClienteLogin:
                 id = dados_cliente['id']
                 nome = dados_cliente['nome']
            return ClienteLogin()
        else:
            print(f"Login falhou: Senha incorreta para CPF {cpf_limpo}.")
            return f"Login falhou: Senha incorreta para o CPF {cpf_limpo}."
    except Exception as e:
        print(f"Erro ao validar login: {e}")
        return "Erro interno ao validar o login."
    finally:
        cursor.close()

# --- Funções de Validação de Cadastro ---

def verificar_cpf_existente(cpf_limpo: str) -> bool:
    """Verifica se um CPF já existe na tabela de clientes."""
    db = get_db()
    cursor = db.cursor()
    try:
        query = "SELECT 1 FROM clientes WHERE cpf = %s"
        cursor.execute(query, (cpf_limpo,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar CPF: {e}")
        return False
    finally:
        cursor.close()

def verificar_email_existente(email: str) -> bool:
    """Verifica se um e-mail já existe na tabela de clientes."""
    db = get_db()
    cursor = db.cursor()
    try:
        query = "SELECT 1 FROM clientes WHERE email = %s"
        cursor.execute(query, (email,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar Email: {e}")
        return False
    finally:
        cursor.close()

# --- Funções Auxiliares de Limpeza de Dados ---

def _limpar_valor_monetario(valor_str: str):
    """
    Converte uma string monetária (ex: 'R$ 1.500,00') 
    para um float (ex: 1500.00).
    """
    if not valor_str:
        return None
    try:
        valor_limpo = valor_str.replace('R$', '').strip().replace('.', '')
        valor_limpo = valor_limpo.replace(',', '.')
        return float(valor_limpo)
    except (ValueError, TypeError):
        return None

def _limpar_cep(cep_str: str):
    """Converte '12345-678' para '12345678'."""
    if not cep_str:
        return None
    return cep_str.replace('-', '').replace('.', '')

def _limpar_telefone(tel_str: str):
    """Converte '(11) 98765-4321' para '11987654321'."""
    if not tel_str:
        return None
    return tel_str.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')


# --- A Função Principal de Criação (CORRIGIDA) ---

def criar_cliente_completo(dados_completos: dict):
    """
    Função transacional para criar um novo cliente, telefone, endereço e conta.
    Segue o schema.sql fornecido.
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # 1. HASH DA SENHA
        senha_hash = generate_password_hash(dados_completos['senha'])
        
        # 2. Limpar dados financeiros e outros
        salario_float = _limpar_valor_monetario(dados_completos.get('salario'))
        patrimonio_float = _limpar_valor_monetario(dados_completos.get('vl_patrimonio'))
        cep_limpo = _limpar_cep(dados_completos.get('cep'))
        telefone_limpo = _limpar_telefone(dados_completos.get('telefone'))

        # 3. INSERT na tabela CLIENTES (sem telefone!)
        sql_cliente = """
            INSERT INTO clientes (
                cpf, rg, nome, data_nascimento, email, salario, 
                vl_patrimonio, id_profissao, senha_hash
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, nome 
        """
        cursor.execute(sql_cliente, (
            dados_completos['cpf'],
            dados_completos.get('rg'),
            dados_completos['nome'],
            dados_completos['nascimento'],
            dados_completos['email'],
            salario_float,
            patrimonio_float,
            dados_completos.get('id_profissao'),
            senha_hash 
        ))
        
        novo_cliente_result = cursor.fetchone()
        if not novo_cliente_result:
            raise Exception("Falha ao criar cliente, não foi possível obter o ID.")
            
        novo_cliente_id = novo_cliente_result[0]
        novo_cliente_nome = novo_cliente_result[1]
        
        # 4. INSERT na tabela TELEFONES (Corrigido)
        sql_telefone = """
            INSERT INTO telefones (id_cliente, numero, tipo)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_telefone, (
            novo_cliente_id, 
            telefone_limpo,
            'celular' # Assume 'celular' como padrão
        ))
        
        # 5. INSERT na tabela ENDERECOS (Corrigido)
        sql_endereco = """
            INSERT INTO enderecos (
                id_cliente, rua, numero, bairro, cidade, 
                estado, cep, complemento
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_endereco, (
            novo_cliente_id,
            dados_completos['rua'],
            dados_completos['numero'],
            dados_completos['bairro'],
            dados_completos['cidade'],
            dados_completos['estado'],
            cep_limpo, # Salva o CEP limpo
            dados_completos.get('complemento')
        ))
        
        # 6. INSERT na tabela CONTAS (Corrigido)
        agencia = '0001'
        numero_conta = f"{random.randint(100000, 999999)}-{random.randint(0, 9)}"
        
        sql_conta = """
            INSERT INTO contas (
                id_cliente, agencia, numero_conta, tipo, saldo, estado
            ) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_conta, (
            novo_cliente_id, 
            agencia, 
            numero_conta, 
            'corrente', # Valor padrão
            0.00,       # Saldo inicial
            'ativa'     # Valor padrão
        ))

        # 7. Se tudo deu certo, COMITA a transação
        db.commit()
        
        # 8. Retorna os dados do novo cliente para a rota (para o login)
        class ClienteStub:
            id = novo_cliente_id
            nome = novo_cliente_nome
            
        return ClienteStub

    except Exception as e:
        # 8. Se algo deu errado, desfaz tudo (ROLLBACK)
        db.rollback()
        print(f"Erro na transação de cadastro: {e}")
        raise Exception(f"Erro ao salvar dados: {e}") 
    finally:
        cursor.close()

def atualizar_perfil_completo(id_cliente: int, dados_formulario):
    """
    Função transacional para ATUALIZAR um cliente, telefone e endereço.
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # 1. Limpar os dados do formulário
        salario_float = _limpar_valor_monetario(dados_formulario.get('salario'))
        cep_limpo = _limpar_cep(dados_formulario.get('cep'))
        telefone_limpo = _limpar_telefone(dados_formulario.get('telefone'))

        # 2. UPDATE na tabela CLIENTES
        # (Atualiza apenas campos que podem ser mudados no perfil)
        sql_cliente = """
            UPDATE clientes 
            SET email = %s, 
                salario = %s,
                id_profissao = %s
            WHERE id = %s
        """
        cursor.execute(sql_cliente, (
            dados_formulario.get('email'),
            salario_float,
            dados_formulario.get('id_profissao'),
            id_cliente
        ))
        
        # 3. UPDATE na tabela TELEFONES
        # (Assume que o cliente só tem um celular para atualizar)
        sql_telefone = """
            UPDATE telefones 
            SET numero = %s 
            WHERE id_cliente = %s AND tipo = 'celular'
        """
        cursor.execute(sql_telefone, (
            telefone_limpo,
            id_cliente
        ))
        
        # 4. UPDATE na tabela ENDERECOS
        # (Assume que o cliente só tem um endereço para atualizar)
        sql_endereco = """
            UPDATE enderecos 
            SET rua = %s, 
                numero = %s, 
                bairro = %s, 
                cidade = %s, 
                estado = %s, 
                cep = %s, 
                complemento = %s
            WHERE id_cliente = %s
        """
        cursor.execute(sql_endereco, (
            dados_formulario.get('rua'),
            dados_formulario.get('numero'),
            dados_formulario.get('bairro'),
            dados_formulario.get('cidade'),
            dados_formulario.get('estado'),
            cep_limpo,
            dados_formulario.get('complemento'),
            id_cliente
        ))

        # 5. Se tudo deu certo, COMITA a transação
        db.commit()

    except Exception as e:
        # 6. Se algo deu errado, desfaz tudo (ROLLBACK)
        db.rollback()
        print(f"Erro na transação de atualização de perfil: {e}", flush=True)
        # Re-levanta o erro para a rota (conta_routes) poder pegá-lo
        raise Exception(f"Erro ao salvar dados: {e}") 
    finally:
        cursor.close()


def excluir_cliente_completo(id_cliente: int):
    """
    Deleta o cliente e todos os dados relacionados em cascata.
    A ordem é crucial para evitar violações de Chave Estrangeira.
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # 1. Obter o ID da conta do cliente
        cursor.execute("SELECT id FROM contas WHERE id_cliente = %s", (id_cliente,))
        resultado_conta = cursor.fetchone()
        if not resultado_conta:
             # O cliente não tem conta, podemos pular para o final
             id_conta = None 
        else:
             id_conta = resultado_conta[0]

        # 2. DELETE em tabelas com FOREIGN KEYS apontando para 'contas'
        if id_conta:
             # Deleta todas as chaves PIX desta conta
             cursor.execute("DELETE FROM chaves_pix WHERE id_conta = %s", (id_conta,))
             # Deleta todas as movimentações desta conta
             cursor.execute("DELETE FROM movimentacoes WHERE id_conta = %s", (id_conta,))
             # Deleta a conta em si
             cursor.execute("DELETE FROM contas WHERE id = %s", (id_conta,))

        # 3. DELETE em tabelas com FOREIGN KEYS apontando para 'clientes'
        # Deleta endereços
        cursor.execute("DELETE FROM enderecos WHERE id_cliente = %s", (id_cliente,))
        # Deleta telefones
        cursor.execute("DELETE FROM telefones WHERE id_cliente = %s", (id_cliente,))

        # 4. DELETE final na tabela 'clientes'
        cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
        
        # 5. Confirma a transação
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(f"ERRO CRÍTICO NA EXCLUSÃO DE CONTA: {e}", flush=True)
        # Re-lança o erro para a rota (conta_routes) tratar
        raise Exception("Falha ao excluir a conta devido a um erro interno.")
    finally:
        cursor.close()

def verificar_senha_autorizacao(id_cliente: int, senha_texto: str) -> bool:
    """
    Verifica se a senha informada corresponde à senha do cliente logado.
    Usado para autorizar transações sensíveis.
    """
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        query = "SELECT senha_hash FROM clientes WHERE id = %s"
        cursor.execute(query, (id_cliente,))
        resultado = cursor.fetchone()
        
        if not resultado:
            return False
            
        return check_password_hash(resultado['senha_hash'], senha_texto.strip())
    except Exception as e:
        print(f"Erro ao verificar senha: {e}", flush=True)
        return False
    finally:
        cursor.close()