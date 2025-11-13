from flask import render_template, Blueprint, request, flash, redirect, url_for, jsonify, session
from src.app.services import cliente_services # Importe seu serviço de cliente
bp = Blueprint('auth', __name__) 

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dados = request.form
        cpf = dados.get('cpf')     # CPF virá com máscara (ex: '123.456.789-00')
        senha = dados.get('senha') # Senha em texto plano
        
        # Chame a função a partir do serviço importado
        cliente = cliente_services.validar_login(cpf, senha)

        if cliente:
            # (Aqui você deve criar a sessão do usuário)
            # session['user_id'] = cliente.id_cliente
            return jsonify({'status': 'sucesso', 'cliente_id': cliente.id_cliente}), 200
        else:
            return jsonify({'status': 'erro', 'mensagem': 'CPF ou senha inválidos'}), 401
    
    # [CORRIGIDO] Se for GET, você deve renderizar a página de login
    return render_template('login.html')

@bp.route('/abrir-conta', methods=['GET', 'POST'])
def abrir_conta():
    if request.method == 'POST':
        # 1. Obter os dados do formulário
        cpf_sujo = request.form['cpf'] # Ex: '123.456.789-00'
        
        # 2. Limpar o CPF (MUITO IMPORTANTE)
        cpf_limpo = cpf_sujo.replace('.', '').replace('-', '') # Ex: '12345678900'
        
        # 3. Chamar o serviço para validar
        if cliente_services.verificar_cpf_existente(cpf_limpo):
            # 4. Se existir, mostrar um erro (flash) e recarregar a página
            flash('Este CPF já está cadastrado. Tente fazer login.', 'error')
            return redirect(url_for('auth.abrir_conta'))
        
        # 5. Se não existir, continue com o cadastro...
        # (Pegue os outros dados: nome, email, etc.)
        # (Salve os dados na sessão para a próxima etapa)
        # session['cadastro_nome'] = request.form['nome-completo']
        # session['cadastro_cpf'] = cpf_limpo
        # ...
        
        return redirect(url_for('auth.abrir_conta_endereco'))

    return render_template('abrir-conta.html')

@bp.route('/abrir-conta-endereco', methods=['GET', 'POST'])
def abrir_conta_endereco():
    if request.method == 'POST':
        dados = session['dados_registro']

        dados.update ({
            'cep': dados.get('cep'),
            'rua': dados.get('rua'),
            'numero': dados.get('numero'),
            'complemento': dados.get('complemento'),
            'bairro': dados.get('bairro'),
            'cidade': dados.get('cidade'),
            'estado': dados.get('estado'),
            'pais': dados.get('pais')
        })

        session['dados_registro'] = dados

        return redirect(url_for('auth.abrir_conta_financeiro'))
    return render_template('abrir-conta-endereco.html')

@bp.route('/abrir-conta-dados-financeiros', methods=['GET', 'POST'])
def abrir_conta_financeiro():
    if request.method == 'POST':
        dados = session['dados_registro']

        dados.update ({
            'rg': dados.get('rg'),
            'profissao': dados.get('profissao'),
            'salario': dados.get('salario'),
            'vl_patrimonio': dados.get('vl_patrimonio'),
        })

        return redirect(url_for('auth.criar_senha_final'))
    return render_template('abrir-conta-dados-financeiros.html')

@bp.route('/paginas-restritas/criar-senha', methods=['GET', 'POST'])
def criar_senha_final():
    if request.method == 'POST':
        dados = session['dados_registro']

        dados.update ({
            'senha': dados.get('senha')
        })

        return redirect(url_for('cliente.area-do-cliente'))
    return render_template('paginas-restritas/criar-senha.html')



@bp.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        # Lógica para enviar e-mail de redefinição...
        return "Link de redefinição enviado!"
    return render_template('esqueci-senha.html')