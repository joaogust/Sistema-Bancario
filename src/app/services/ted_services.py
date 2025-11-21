from src.app.db import get_db
from src.app.data_classes.ted import TED
from decimal import Decimal
from datetime import datetime, time

def validar_horario_ted() -> bool:
    """Valida se está dentro do horário comercial para TED"""
    agora = datetime.now().time()
    horario_inicio = time(6, 0)   # 06:00
    horario_fim = time(17, 0)     # 17:00
    
    return horario_inicio <= agora <= horario_fim

def validar_limite_ted_diario(id_conta: int, valor: Decimal) -> bool:
    """Valida se o limite diário de TED não foi excedido"""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            SELECT COALESCE(SUM(valor), 0) 
            FROM movimentacoes 
            WHERE id_conta = %s 
            AND tipo = 'TED' 
            AND DATE(data_hora) = CURRENT_DATE
        """, (id_conta,))
        
        total_hoje = cursor.fetchone()[0] or Decimal('0')
        limite_diario = Decimal('10000.00')  # R$ 10.000,00
        
        return (total_hoje + valor) <= limite_diario
    finally:
        cursor.close()

def realizar_ted(id_conta_origem: int, dados_ted: TED) -> dict:
    """
    Executa uma TED com validações completas.
    Retorna dict com sucesso e mensagem.
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Validações iniciais
        if dados_ted.valor <= Decimal('0'):
            return {'sucesso': False, 'mensagem': 'O valor deve ser positivo.'}
        
        if dados_ted.valor < Decimal('1.00'):
            return {'sucesso': False, 'mensagem': 'O valor mínimo para TED é R$ 1,00.'}
        
        # Valida limite máximo por transação
        if dados_ted.valor > Decimal('10000.00'):
            return {'sucesso': False, 'mensagem': 'Valor máximo por transação TED é R$ 10.000,00.'}
        
        # Valida limite diário
        if not validar_limite_ted_diario(id_conta_origem, dados_ted.valor):
            return {'sucesso': False, 'mensagem': 'Limite diário de TED excedido.'}
        
        # Valida horário comercial
        if not validar_horario_ted():
            return {'sucesso': False, 'mensagem': 'TED disponível apenas das 06h às 17h em dias úteis.'}

        # 1. Verifica conta origem (com bloqueio)
        cursor.execute("""
            SELECT saldo, estado 
            FROM contas 
            WHERE id = %s FOR UPDATE
        """, (id_conta_origem,))
        
        resultado = cursor.fetchone()
        if not resultado:
            return {'sucesso': False, 'mensagem': 'Conta de origem não encontrada.'}
            
        saldo_atual, estado_conta = resultado
        
        if estado_conta != 'ativa':
            return {'sucesso': False, 'mensagem': 'Sua conta não está ativa.'}
        
        if saldo_atual < dados_ted.valor:
            return {'sucesso': False, 'mensagem': 'Saldo insuficiente.'}

        # 2. Debita o valor
        novo_saldo = saldo_atual - dados_ted.valor
        cursor.execute("UPDATE contas SET saldo = %s WHERE id = %s", 
                      (novo_saldo, id_conta_origem))

        # 3. Registra a movimentação - CORREÇÃO: removida a coluna 'descricao' se existir
        sql_movimentacao = """
            INSERT INTO movimentacoes (
                valor, tipo, id_conta, 
                num_conta_destino, agencia_destino, tipo_conta_destino, 
                instituicao_destino, nome_destino, cpf_cnpj_destino
            )
            VALUES (%s, 'TED', %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_movimentacao, (
            dados_ted.valor, 
            id_conta_origem,
            dados_ted.num_conta_destino,
            dados_ted.agencia_destino,
            dados_ted.tipo_conta_destino,
            dados_ted.instituicao_destino,
            dados_ted.nome_destino,
            dados_ted.cpf_cnpj_destino
        ))

        db.commit()
        
        return {
            'sucesso': True, 
            'mensagem': 'TED agendado com sucesso! O valor será transferido até o final do dia útil.'
        }

    except Exception as e:
        db.rollback()
        print(f"Erro ao realizar TED: {e}", flush=True)
        return {'sucesso': False, 'mensagem': f'Erro interno ao processar TED: {str(e)}'}
    finally:
        cursor.close()