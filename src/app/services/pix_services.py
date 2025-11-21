from src.app.db import get_db
from src.app.data_classes.pix import PIX
from decimal import Decimal
import re
from datetime import datetime, time

def detectar_tipo_chave(chave: str) -> str:
    """Detecta automaticamente o tipo da chave PIX"""
    if not chave:
        return 'aleatoria'
    
    chave = chave.strip().lower()
    
    # CPF (11 dígitos)
    if re.match(r'^\d{11}$', chave):
        return 'cpf'
    
    # E-mail
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', chave):
        return 'email'
    
    # Celular (com DDI e DDD)
    if re.match(r'^\+?55\d{10,11}$', chave.replace(' ', '').replace('-', '')):
        return 'celular'
    
    # Chave aleatória (UUID ou similar)
    if re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', chave):
        return 'aleatoria'
    
    return 'aleatoria'

def validar_limite_pix_diario(id_conta: int, valor: Decimal) -> bool:
    """Valida se o limite diário de PIX não foi excedido"""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            SELECT COALESCE(SUM(valor), 0) 
            FROM movimentacoes 
            WHERE id_conta = %s 
            AND tipo = 'PIX' 
            AND DATE(data_hora) = CURRENT_DATE
        """, (id_conta,))
        
        total_hoje = cursor.fetchone()[0] or Decimal('0')
        limite_diario = Decimal('5000.00')  # R$ 5.000,00
        
        return (total_hoje + valor) <= limite_diario
    finally:
        cursor.close()

def realizar_pix(id_conta_origem: int, dados_pix: PIX) -> dict:
    """
    Executa um PIX com validações completas.
    Retorna dict com sucesso e mensagem.
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Validações iniciais
        if dados_pix.valor <= Decimal('0'):
            return {'sucesso': False, 'mensagem': 'O valor deve ser positivo.'}
        
        if dados_pix.valor < Decimal('0.01'):
            return {'sucesso': False, 'mensagem': 'O valor mínimo é R$ 0,01.'}
        
        # Valida limite máximo por transação
        if dados_pix.valor > Decimal('5000.00'):
            return {'sucesso': False, 'mensagem': 'Valor máximo por transação PIX é R$ 5.000,00.'}
        
        # Valida limite diário
        if not validar_limite_pix_diario(id_conta_origem, dados_pix.valor):
            return {'sucesso': False, 'mensagem': 'Limite diário de PIX excedido.'}

        # 1. Verifica conta origem (com bloqueio para evitar race condition)
        cursor.execute("""
            SELECT c.saldo, c.estado, cl.nome 
            FROM contas c 
            JOIN clientes cl ON c.id_cliente = cl.id 
            WHERE c.id = %s FOR UPDATE
        """, (id_conta_origem,))
        
        res_origem = cursor.fetchone()
        if not res_origem:
            return {'sucesso': False, 'mensagem': 'Conta origem não encontrada.'}
        
        saldo_atual, estado_conta, nome_cliente = res_origem
        
        if estado_conta != 'ativa':
            return {'sucesso': False, 'mensagem': 'Sua conta não está ativa.'}
        
        if saldo_atual < dados_pix.valor:
            return {'sucesso': False, 'mensagem': 'Saldo insuficiente.'}

        # 2. Busca conta destino pela chave PIX
        cursor.execute("""
            SELECT c.id, c.estado, cl.nome 
            FROM chaves_pix cp
            JOIN contas c ON cp.id_conta = c.id
            JOIN clientes cl ON c.id_cliente = cl.id
            WHERE cp.chave = %s AND c.estado = 'ativa'
        """, (dados_pix.chave_destino,))
        
        conta_destino = cursor.fetchone()
        transferencia_interna = bool(conta_destino)

        # 3. Processa o Débito na Origem
        novo_saldo_origem = saldo_atual - dados_pix.valor
        cursor.execute("UPDATE contas SET saldo = %s WHERE id = %s", 
                      (novo_saldo_origem, id_conta_origem))
        
        # Registra a saída - CORREÇÃO: removida a coluna 'descricao'
        cursor.execute("""
            INSERT INTO movimentacoes (valor, tipo, id_conta, chave_destino)
            VALUES (%s, 'PIX', %s, %s)
        """, (dados_pix.valor, id_conta_origem, dados_pix.chave_destino))

        # 4. Se for interna, Processa o Crédito no Destino
        if transferencia_interna:
            id_conta_destino, estado_destino, nome_destino = conta_destino
            
            if id_conta_destino == id_conta_origem:
                db.rollback()
                return {'sucesso': False, 'mensagem': 'Não é possível fazer PIX para a mesma conta.'}
            
            if estado_destino != 'ativa':
                db.rollback()
                return {'sucesso': False, 'mensagem': 'Conta destino não está ativa.'}
            
            # Credita na conta destino
            cursor.execute("UPDATE contas SET saldo = saldo + %s WHERE id = %s", 
                          (dados_pix.valor, id_conta_destino))
            
            # Registra a entrada para o destino - CORREÇÃO: removida a coluna 'descricao'
            cursor.execute("""
                INSERT INTO movimentacoes (valor, tipo, id_conta, chave_destino)
                VALUES (%s, 'PIX', %s, %s)
            """, (dados_pix.valor, id_conta_destino, dados_pix.chave_destino))

        db.commit()
        
        mensagem = 'Transferência PIX realizada com sucesso!'
        if transferencia_interna:
            mensagem += f' Valor creditado para {nome_destino}.'
        else:
            mensagem += ' Aguardando confirmação do destinatário.'
        
        return {'sucesso': True, 'mensagem': mensagem, 'interno': transferencia_interna}

    except Exception as e:
        db.rollback()
        print(f"Erro ao realizar PIX: {e}", flush=True)
        return {'sucesso': False, 'mensagem': f'Erro interno ao processar PIX: {str(e)}'}
    finally:
        cursor.close()