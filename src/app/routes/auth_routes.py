from flask import render_template, Blueprint, request, flash, redirect, url_for, session
from src.app.services import cliente_services, profissao_services

# Define o Blueprint com o prefixo '/auth'
bp = Blueprint('auth', __name__, url_prefix='/auth')

# --- ROTA DE LOGIN ---
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        # .strip() remove espaços em branco extras que causam erro de senha
        senha = request.form.get('senha', '').strip()

        # O resultado pode ser o Cliente (Objeto) OU uma mensagem de erro (String)
        resultado = cliente_services.validar_login(cpf, senha)

        if isinstance(resultado, str):
            # É uma string, então é uma mensagem de erro. Mostra na tela.
            flash(resultado, 'danger')
            return redirect(url_for('auth.login'))
        
        elif resultado:
            # Não é string e não é None, então é o objeto Cliente. Sucesso!
            cliente = resultado
            session['user_id'] = cliente.id
            session.modified = True
            flash(f'Bem-vindo(a) de volta, {cliente.nome}!', 'success')
            return redirect(url_for('conta.area_do_cliente'))
            
        else:
            # Caso de segurança (não deve acontecer com o novo serviço)
            flash('Erro desconhecido no login.', 'danger')
            return redirect(url_for('auth.login'))
            
    return render_template('login.html')

# --- ROTA DE ESQUECI SENHA ---
@bp.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        flash('Link de redefinição enviado para seu e-mail.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('esqueci-senha.html')


# ==========================================================
#                FLUXO DE ABERTURA DE CONTA
# ==========================================================

# --- ETAPA 1: DADOS PESSOAIS ---
@bp.route('/abrir-conta', methods=['GET', 'POST'])
def abrir_conta():
    if request.method == 'POST':
        cpf_sujo = request.form.get('cpf')
        cpf_limpo = cpf_sujo.replace('.', '').replace('-', '')
        
        if cliente_services.verificar_cpf_existente(cpf_limpo):
            flash('Este CPF já está cadastrado. Tente fazer login.', 'error')
            return render_template('abrir-conta.html')
        
        dados_pessoais = {
            'nome': request.form.get('nome-completo'),
            'telefone': request.form.get('telefone'),
            'email': request.form.get('email'),
            'cpf': cpf_limpo, 
            'nascimento': request.form.get('nascimento')
        }
        
        session['dados_registro'] = dados_pessoais
        session.modified = True
        
        return redirect(url_for('auth.abrir_conta_endereco'))
    
    return render_template('abrir-conta.html')

# --- ETAPA 2: ENDEREÇO ---
@bp.route('/abrir-conta-endereco', methods=['GET', 'POST'])
def abrir_conta_endereco():
    if 'dados_registro' not in session:
        flash('Sua sessão expirou. Por favor, comece novamente.', 'warning')
        return redirect(url_for('auth.abrir_conta'))

    if request.method == 'POST':
        dados = session['dados_registro']
        dados_endereco = {
            'cep': request.form.get('cep'),
            'rua': request.form.get('rua'),
            'numero': request.form.get('numero'),
            'complemento': request.form.get('complemento'),
            'bairro': request.form.get('bairro'),
            'cidade': request.form.get('cidade'),
            'estado': request.form.get('estado'),
            'pais': request.form.get('pais')
        }
        dados.update(dados_endereco)
        session['dados_registro'] = dados
        session.modified = True
        
        return redirect(url_for('auth.abrir_conta_financeiro'))
    
    return render_template('abrir-conta-endereco.html')

# --- ETAPA 3: DADOS FINANCEIROS ---
@bp.route('/abrir-conta-dados-financeiros', methods=['GET', 'POST'])
def abrir_conta_financeiro():
    if 'dados_registro' not in session:
        flash('Sua sessão expirou. Por favor, comece novamente.', 'warning')
        return redirect(url_for('auth.abrir_conta'))

    if request.method == 'POST':
        dados = session['dados_registro']
        dados_financeiros = {
            'rg': request.form.get('rg'),
            'id_profissao': request.form.get('id_profissao'),
            'salario': request.form.get('salario'),
            'vl_patrimonio': request.form.get('vl_patrimonio')
        }
        dados.update(dados_financeiros)
        session['dados_registro'] = dados
        session.modified = True
        
        return redirect(url_for('auth.abrir_conta_senha')) 
    
    try:
        lista_de_profissoes = profissao_services.listar_profissoes()
    except Exception as e:
        flash(f'Erro ao carregar dados do servidor: {e}', 'danger')
        lista_de_profissoes = []

    return render_template(
        'abrir-conta-dados-financeiros.html', 
        profissoes=lista_de_profissoes 
    )

# --- ETAPA 4: MOSTRAR PÁGINA DE SENHA (GET) ---
@bp.route('/abrir-conta-senha', methods=['GET'])
def abrir_conta_senha():
    if 'dados_registro' not in session:
        flash('Sua sessão expirou. Por favor, comece novamente.', 'warning')
        return redirect(url_for('auth.abrir_conta'))
        
    return render_template('paginas-restritas/criar-senha.html') 

# --- ETAPA 4: PROCESSAR SENHA E FINALIZAR CADASTRO (POST) ---
@bp.route('/paginas-restritas/criar-senha', methods=['POST'])
def criar_senha_final():
    if 'dados_registro' not in session:
        flash('Sua sessão expirou. Por favor, comece novamente.', 'warning')
        return redirect(url_for('auth.abrir_conta'))

    # .strip() remove espaços extras para garantir que a senha salva seja limpa
    senha = request.form.get('senha', '').strip()
    senha_confirm = request.form.get('senha_confirm', '').strip()
    
    if not senha or not senha_confirm or len(senha) != 6 or senha != senha_confirm:
        flash('As senhas não conferem ou são inválidas. A senha deve ter 6 números.', 'error')
        return redirect(url_for('auth.abrir_conta_senha'))

    # === SALVAR NO BANCO ===
    try:
        dados_completos = session['dados_registro']
        dados_completos['senha'] = senha
        
        novo_cliente = cliente_services.criar_cliente_completo(dados_completos)
        
        session.pop('dados_registro', None)
        
        # Redireciona para o LOGIN com mensagem de sucesso
        flash(f'Conta para {novo_cliente.nome} criada com sucesso! Por favor, faça o login.', 'success')
        return redirect(url_for('auth.login'))

    except Exception as e:
        print(f"ERRO CRÍTICO AO FINALIZAR CADASTRO: {e}")
        flash(f'Ocorreu um erro ao criar sua conta. Tente novamente.', 'danger')
        return redirect(url_for('auth.abrir_conta'))