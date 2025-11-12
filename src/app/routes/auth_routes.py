from flask import render_template, Blueprint, request, redirect, url_for, jsonify, session
from src.app.services.auth_services import *

bp = Blueprint('auth', __name__) 

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dados = request.form
        cpf = dados.get('cpf')
        senha = dados.get('senha')
        cliente = validar_login(cpf, senha)

        if cliente:
            return jsonify({'status': 'sucesso', 'cliente_id': cliente.id}), 200
        else:
            return jsonify({'status': 'erro', 'mensagem': 'CPF ou senha inválidos'}), 401
    return None

@bp.route('/abrir-conta', methods=['GET', 'POST']) # Aceita GET e POST
def abrir_conta():
    if request.method == 'POST':
        dados = request.form

        dados_pessoais = {
            "nome": dados.get('nome'),
            "telefone": dados.get('telefone'),
            "email": dados.get('email'),
            "cpf": dados.get('cpf'),
            "nascimento": dados.get('nascimento')
        }

        session['dados_registro'] = dados_pessoais

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

# (Você também precisará das rotas para criar/redefinir a senha)
@bp.route('/criar-senha-final', methods=['GET', 'POST'])
def criar_senha_final():
    # Esta rota deve ter os inputs name="senha" e name="senha_confirm"
    # para o seu JavaScript de validação funcionar.
    if request.method == 'POST':
        senha = request.form['senha']
        # Salvar a senha (com hash!) e finalizar o cadastro
        return redirect(url_for('auth.login'))
    return render_template('criar-senha.html') # Crie este template