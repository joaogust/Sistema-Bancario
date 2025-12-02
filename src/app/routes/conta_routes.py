from flask import render_template, Blueprint, request, redirect, url_for, session, flash, jsonify
from decimal import Decimal
# Importa OS DOIS serviços
from src.app.data_classes.pix import PIX
from src.app.data_classes.ted import TED
from src.app.services import cliente_services, conta_services, endereco_services, telefone_services, profissao_services, chave_pix_services, movimentacao_services, pix_services, ted_services

bp = Blueprint('conta', __name__, url_prefix='/conta')

# --- FUNÇÃO AUXILIAR PARA CONVERTER DINHEIRO ---
def converter_valor(valor_bruto):
    """
    Converte strings como '1.200,50', '1200.50', 'R$ 100' para Decimal.
    """
    try:
        valor_str = str(valor_bruto).replace('R$', '').replace(' ', '').strip()
        
        # Lógica para detectar formato BR (1.000,00)
        if ',' in valor_str:
            # Se tem vírgula, assume que é decimal
            # Remove pontos de milhar e troca vírgula por ponto
            valor_str = valor_str.replace('.', '').replace(',', '.')
        
        # Se não tem vírgula, assume formato padrão (1000.50) e não faz nada
        
        print(f"DEBUG - Convertendo: '{valor_bruto}' -> '{valor_str}'", flush=True)
        return Decimal(valor_str)
    except Exception as e:
        print(f"DEBUG - Erro ao converter valor: {e}", flush=True)
        raise ValueError(f"Valor inválido: {valor_bruto}")

# ==========================
# ROTAS PRINCIPAIS
# ==========================

@bp.route('/area-do-cliente')
def area_do_cliente():
    user_id = session.get('user_id')
    
    if not user_id:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))

    try:
        # 1. Busca os dados do cliente
        cliente = cliente_services.get_cliente(user_id)
        # 2. Busca os dados da conta
        conta = conta_services.get_conta_by_cliente_id(user_id)
        
        if not cliente or not conta:
            session.pop('user_id', None)
            flash('Usuário ou conta não encontrados.', 'danger')
            return redirect(url_for('auth.login'))

        # Passa AMBOS os objetos para o template
        return render_template(
            'paginas-restritas/area-do-cliente.html',
            cliente=cliente,
            conta=conta 
        )
        
    except Exception as e:
        print(f"Erro ao carregar dados do cliente/conta: {e}", flush=True)
        flash('Ocorreu um erro ao carregar seus dados.', 'danger')
        return redirect(url_for('auth.login'))

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))

# ==========================
# EXTRATO
# ==========================

@bp.route('/extrato')
def extrato():
    user_id = session.get('user_id')
    if not user_id:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
    
    try:
        cliente = cliente_services.get_cliente(user_id)
        conta = conta_services.get_conta_by_cliente_id(user_id)
        
        if not cliente or not conta:
             return redirect(url_for('auth.login'))
             
        # Busca as movimentações reais
        movimentacoes = movimentacao_services.listar_movimentacoes_por_conta(conta.id)
        
        return render_template(
            'paginas-restritas/extrato-cliente.html',
            cliente=cliente,
            conta=conta,
            movimentacoes=movimentacoes
        )
    except Exception as e:
        print(f"Erro ao carregar extrato: {e}", flush=True)
        flash('Erro ao carregar extrato.', 'danger')
        return redirect(url_for('auth.login'))

# ==========================
# TRANSFERÊNCIAS (FLUXO DE 3 ETAPAS)
# ==========================

@bp.route('/transferencia', methods=['GET'])
def transferencia():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    try:
        cliente = cliente_services.get_cliente(user_id)
        conta = conta_services.get_conta_by_cliente_id(user_id)
        
        if not cliente or not conta:
            return redirect(url_for('auth.login'))
            
        return render_template(
            'paginas-restritas/realizar-transferencia.html', 
            cliente=cliente, 
            conta=conta
        )
    except Exception as e:
        print(f"Erro ao carregar tela de transferência: {e}", flush=True)
        flash('Erro ao carregar página de transferência.', 'danger')
        return redirect(url_for('auth.login'))

# --- ETAPA 1: VALIDAR DADOS PIX ---
@bp.route('/transferencia/validar/pix', methods=['POST'])
def validar_pix():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    try:
        # Obter dados do formulário - REMOVIDO: descricao
        chave_destino = request.form.get('chave_destino')
        valor = request.form.get('valor')
        # REMOVIDO: descricao = request.form.get('descricao', '')
        
        # Validações básicas
        if not all([chave_destino, valor]):
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        # Converter valor
        valor_decimal = converter_valor(valor)
        
        # Validar limites
        if valor_decimal > Decimal('5000.00'):
            flash('Valor máximo para PIX é R$ 5.000,00.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        if valor_decimal <= Decimal('0'):
            flash('O valor deve ser positivo.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        # Buscar conta do usuário
        conta_origem = conta_services.get_conta_by_cliente_id(user_id)
        if not conta_origem:
            flash('Conta não encontrada.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        # Verificar saldo
        if conta_origem.saldo < valor_decimal:
            flash('Saldo insuficiente.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        # Armazenar dados na sessão para próxima etapa - REMOVIDO: descricao
        dados_pix = {
            'tipo_transacao': 'PIX',
            'chave_destino': chave_destino,
            'valor': str(valor_decimal)
            # REMOVIDO: 'descricao': descricao
        }
        session['transacao_pendente'] = dados_pix
        
        cliente = cliente_services.get_cliente(user_id)
        return render_template(
            'paginas-restritas/transferencia-Pix-senha.html', 
            cliente=cliente, 
            dados=dados_pix
        )
            
    except ValueError as ve:
        flash(f'Erro no valor: {str(ve)}', 'danger')
        return redirect(url_for('conta.transferencia'))
    except Exception as e:
        print(f"Erro na validação PIX: {e}", flush=True)
        flash('Erro ao validar transferência.', 'danger')
        return redirect(url_for('conta.transferencia'))

# --- ETAPA 1: VALIDAR DADOS TED ---
@bp.route('/transferencia/validar/ted', methods=['POST'])
def validar_ted():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    try:
        # Obter dados do formulário
        instituicao_destino = request.form.get('instituicao_destino')
        agencia_destino = request.form.get('agencia_destino')
        num_conta_destino = request.form.get('num_conta_destino')
        tipo_conta_destino = request.form.get('tipo_conta_destino')
        nome_destino = request.form.get('nome_destino')
        cpf_cnpj_destino = request.form.get('cpf_cnpj_destino')
        valor = request.form.get('valor')
        
        # Validações básicas
        campos_obrigatorios = [
            instituicao_destino, agencia_destino, num_conta_destino,
            tipo_conta_destino, nome_destino, cpf_cnpj_destino, valor
        ]
        
        if not all(campos_obrigatorios):
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        # Converter valor
        valor_decimal = converter_valor(valor)
        
        # Validar limites
        if valor_decimal > Decimal('10000.00'):
            flash('Valor máximo para TED é R$ 10.000,00.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        if valor_decimal < Decimal('1.00'):
            flash('Valor mínimo para TED é R$ 1,00.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        # Buscar conta do usuário
        conta_origem = conta_services.get_conta_by_cliente_id(user_id)
        if not conta_origem:
            flash('Conta não encontrada.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        # Verificar saldo
        if conta_origem.saldo < valor_decimal:
            flash('Saldo insuficiente.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        # Armazenar dados na sessão para próxima etapa
        dados_ted = {
            'tipo_transacao': 'TED',
            'instituicao_destino': instituicao_destino,
            'agencia_destino': agencia_destino,
            'num_conta_destino': num_conta_destino,
            'tipo_conta_destino': tipo_conta_destino,
            'nome_destino': nome_destino,
            'cpf_cnpj_destino': cpf_cnpj_destino,
            'valor': str(valor_decimal)
        }
        session['transacao_pendente'] = dados_ted
        
        cliente = cliente_services.get_cliente(user_id)
        return render_template(
            'paginas-restritas/transferencia-TED-senha.html', 
            cliente=cliente, 
            dados=dados_ted
        )
            
    except ValueError as ve:
        flash(f'Erro no valor: {str(ve)}', 'danger')
        return redirect(url_for('conta.transferencia'))
    except Exception as e:
        print(f"Erro na validação TED: {e}", flush=True)
        flash('Erro ao validar transferência.', 'danger')
        return redirect(url_for('conta.transferencia'))

# --- ETAPA 2: CONFIRMAR COM SENHA ---
@bp.route('/transferencia/confirmar', methods=['POST'])
def confirmar_transferencia():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    try:
        senha_digitada = request.form.get('senha_transacao')
        dados = session.get('transacao_pendente')

        if not dados:
            flash('Sessão expirada. Inicie novamente.', 'warning')
            return redirect(url_for('conta.transferencia'))

        # 1. Verifica Senha
        if not cliente_services.verificar_senha_autorizacao(user_id, senha_digitada):
            flash('Senha incorreta. Transação cancelada.', 'danger')
            cliente = cliente_services.get_cliente(user_id)
            
            if dados['tipo_transacao'] == 'TED':
                return render_template(
                    'paginas-restritas/transferencia-TED-senha.html', 
                    cliente=cliente, 
                    dados=dados
                )
            elif dados['tipo_transacao'] == 'PIX':
                return render_template(
                    'paginas-restritas/transferencia-Pix-senha.html', 
                    cliente=cliente, 
                    dados=dados
                )

        # 2. Buscar conta
        conta = conta_services.get_conta_by_cliente_id(user_id)
        if not conta:
            flash('Conta não encontrada.', 'danger')
            return redirect(url_for('conta.transferencia'))
        
        # 3. Converter valor
        valor_decimal = Decimal(dados['valor'])
        
        # 4. Executar transferência
        if dados['tipo_transacao'] == 'TED':
            obj_ted = TED(
                valor=valor_decimal,
                instituicao_destino=dados['instituicao_destino'],
                agencia_destino=dados['agencia_destino'],
                num_conta_destino=dados['num_conta_destino'],
                tipo_conta_destino=dados['tipo_conta_destino'],
                nome_destino=dados['nome_destino'],
                cpf_cnpj_destino=dados['cpf_cnpj_destino']
            )
            resultado = ted_services.realizar_ted(conta.id, obj_ted)
        
        elif dados['tipo_transacao'] == 'PIX':
            # CORREÇÃO: Criar objeto PIX sem o campo descricao
            obj_pix = PIX(
                valor=valor_decimal,
                chave_destino=dados['chave_destino']
                # REMOVIDO: descricao=dados.get('descricao', '')
            )
            resultado = pix_services.realizar_pix(conta.id, obj_pix)

        # 5. Verificar resultado
        if resultado['sucesso']:
            session.pop('transacao_pendente', None)
            return redirect(url_for('conta.transferencia_concluida'))
        else:
            flash(f'Erro na transferência: {resultado["mensagem"]}', 'danger')
            return redirect(url_for('conta.transferencia'))

    except Exception as e:
        print(f"Erro crítico na transação: {e}", flush=True)
        flash('Erro ao processar transferência.', 'danger')
        return redirect(url_for('conta.transferencia'))

# --- ETAPA 3: TELA DE CONCLUSÃO ---
@bp.route('/transferencia/concluida')
def transferencia_concluida():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    try:
        cliente = cliente_services.get_cliente(user_id)
        conta = conta_services.get_conta_by_cliente_id(user_id)
        
        if not cliente or not conta:
            return redirect(url_for('auth.login'))
            
        return render_template(
            'paginas-restritas/transferencia-concluida.html', 
            cliente=cliente,
            conta=conta
        )
    except Exception as e:
        print(f"Erro ao carregar página de conclusão: {e}", flush=True)
        flash('Erro ao carregar página.', 'danger')
        return redirect(url_for('conta.transferencia'))


@bp.route('/sacar', methods=['POST'])
def sacar():
    user_id = session.get('user_id')
    if not user_id: return redirect(url_for('auth.login'))
    
    try:
        conta = conta_services.get_conta_by_cliente_id(user_id)
        if not conta: raise ValueError("Conta não encontrada.")
        
        # O valor é pego do formulário
        valor_bruto = request.form.get('valor_saque')
        valor_decimal = converter_valor(valor_bruto)

        # Chama a função do serviço que executa a stored procedure SQL
        movimentacao_services.realizar_saque_db(conta.id, valor_decimal)

        flash(f'Saque de R$ {valor_decimal} realizado com sucesso!', 'success')
        return redirect(url_for('conta.area_do_cliente'))

    except ValueError as ve:
        # Erro de Saldo Insuficiente ou Valor Inválido
        flash(f'Erro no saque: {ve}', 'danger')
        return redirect(url_for('conta.area_do_cliente'))
    except Exception as e:
        print(f"Erro ao processar saque: {e}", flush=True)
        flash('Erro ao processar o saque. Verifique o valor ou tente mais tarde.', 'danger')
        return redirect(url_for('conta.area_do_cliente'))
    
# ==========================
# CHAVES PIX
# ==========================

@bp.route('/chaves-pix', methods=['GET', 'POST'])
def chaves_pix():
    user_id = session.get('user_id')
    if not user_id:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
    
    try:
        cliente = cliente_services.get_cliente(user_id)
        conta = conta_services.get_conta_by_cliente_id(user_id)
        
        if not cliente or not conta:
             return redirect(url_for('auth.login'))

        # LÓGICA DO POST (CADASTRAR CHAVE)
        if request.method == 'POST':
            tipo_chave = request.form.get('tipo')
            
            valor_chave = None
            
            # Define o valor da chave baseado no tipo escolhido
            if tipo_chave == 'cpf':
                valor_chave = cliente.cpf
            elif tipo_chave == 'email':
                valor_chave = cliente.email
            elif tipo_chave == 'celular':
                # Busca telefone celular do cliente
                telefone = telefone_services.get_telefone_by_cliente_id(user_id)
                if telefone and telefone.tipo == 'celular':
                    valor_chave = telefone.numero
                else:
                    flash('Nenhum número de celular cadastrado.', 'warning')
                    return redirect(url_for('conta.chaves_pix'))
            elif tipo_chave == 'aleatoria':
                valor_chave = None  # O service vai gerar automaticamente
            
            try:
                resultado = chave_pix_services.criar_chave_pix(conta.id, tipo_chave, valor_chave)
                if resultado['sucesso']:
                    flash('Chave PIX cadastrada com sucesso!', 'success')
                else:
                    flash(f'Erro ao cadastrar chave: {resultado["mensagem"]}', 'danger')
            except Exception as e:
                flash(f'Erro ao cadastrar chave: {str(e)}', 'danger')
                
            return redirect(url_for('conta.chaves_pix'))

        # LÓGICA DO GET (LISTAR CHAVES)
        lista_chaves = chave_pix_services.listar_chaves_por_conta(conta.id)
        
        return render_template(
            'paginas-restritas/chaves-pix.html',
            cliente=cliente,
            conta=conta,
            chaves=lista_chaves
        )
    except Exception as e:
        print(f"Erro ao carregar chaves PIX: {e}", flush=True)
        flash('Erro ao carregar chaves PIX.', 'danger')
        return redirect(url_for('auth.login'))

@bp.route('/chaves-pix/excluir/<int:id_chave>', methods=['POST'])
def excluir_chave_pix(id_chave):
    user_id = session.get('user_id')
    if not user_id:
        flash('Você precisa estar logado para acessar.', 'warning')
        return redirect(url_for('auth.login'))

    try:
        conta = conta_services.get_conta_by_cliente_id(user_id)

        if not conta:
            flash('Conta não encontrada.', 'danger')
            return redirect(url_for('conta.chaves_pix'))

        resultado = chave_pix_services.excluir_chave_pix(id_chave, conta.id)
        
        if resultado['sucesso']:
            flash('Chave PIX excluída com sucesso!', 'success')
        else:
            flash(f'Erro ao excluir chave: {resultado["mensagem"]}', 'danger')
            
        return redirect(url_for('conta.chaves_pix'))

    except Exception as e:
        flash(f'Erro ao excluir chave: {str(e)}', 'danger')
        return redirect(url_for('conta.chaves_pix'))

# ==========================
# PERFIL DO USUÁRIO
# ==========================

@bp.route('/meu-perfil', methods=['GET', 'POST'])
def meu_perfil():
    user_id = session.get('user_id')
    if not user_id:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
    
    try:
        if request.method == 'POST':
            try:
                dados_formulario = request.form
                resultado = cliente_services.atualizar_perfil_completo(user_id, dados_formulario)
                
                if resultado['sucesso']:
                    flash('Dados atualizados com sucesso!', 'success')
                else:
                    flash(f'Erro ao atualizar dados: {resultado["mensagem"]}', 'danger')
                    
                return redirect(url_for('conta.meu_perfil'))
            except Exception as e:
                flash(f'Erro ao atualizar dados: {str(e)}', 'danger')

        # GET
        cliente = cliente_services.get_cliente(user_id)
        endereco = endereco_services.get_endereco_by_cliente_id(user_id)
        telefone = telefone_services.get_telefone_by_cliente_id(user_id)
        profissoes = profissao_services.listar_profissoes()

        if not cliente:
             return redirect(url_for('auth.login'))

        # Formatações para exibição
        if cliente and cliente.cpf:
            cliente.cpf_formatado = f"{cliente.cpf[:3]}.{cliente.cpf[3:6]}.{cliente.cpf[6:9]}-{cliente.cpf[9:]}"
        else:
            cliente.cpf_formatado = ""

        if telefone and telefone.numero:
            num = telefone.numero
            telefone.numero_formatado = f"({num[:2]}) {num[2:7]}-{num[7:]}"
        else:
            telefone.numero_formatado = ""

        return render_template(
            'paginas-restritas/meu-perfil.html',
            cliente=cliente,
            endereco=endereco,
            telefone=telefone,
            profissoes=profissoes
        )
    except Exception as e:
        print(f"Erro ao carregar perfil: {e}", flush=True)
        flash(f'Erro ao carregar página: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))

@bp.route('/deletar-conta', methods=['POST'])
def deletar_conta():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    senha_digitada = request.form.get('senha_confirmacao')
    
    try:
        # 1. Verifica Senha
        if not cliente_services.verificar_senha_autorizacao(user_id, senha_digitada):
            flash('Senha incorreta. Exclusão de conta cancelada.', 'danger')
            return redirect(url_for('conta.meu_perfil'))

        # 2. Exclui em Cascata
        resultado = cliente_services.excluir_cliente_completo(user_id)
        
        if resultado['sucesso']:
            # 3. Desloga e redireciona
            session.pop('user_id', None)
            flash('Sua conta foi excluída permanentemente.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash(f'Erro ao excluir conta: {resultado["mensagem"]}', 'danger')
            return redirect(url_for('conta.meu_perfil'))
        
    except ValueError as ve:
        flash(f'Erro de segurança: {str(ve)}', 'warning')
        return redirect(url_for('conta.meu_perfil'))
    except Exception as e:
        print(f"ERRO AO EXCLUIR CONTA: {e}", flush=True)
        flash('Erro crítico ao tentar excluir sua conta.', 'danger')
        return redirect(url_for('conta.meu_perfil'))