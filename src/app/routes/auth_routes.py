# Lembre-se de importar 'request', 'redirect', 'url_for'
from flask import render_template, Blueprint, request, redirect, url_for

# 1. Mude o nome do blueprint para 'auth'
bp = Blueprint('auth', __name__) 

@bp.route('/login', methods=['GET', 'POST']) # Aceita GET e POST
def login():
    if request.method == 'POST':
        # Sua lógica de login aqui...
        cpf = request.form['cpf']
        return f"Logando com {cpf}..."
    return render_template('login.html') # Mostra a página de login

@bp.route('/abrir-conta', methods=['GET', 'POST']) # Aceita GET e POST
def abrir_conta():
    if request.method == 'POST':
        # Sua lógica de cadastro aqui...
        nome = request.form['nome-completo']
        # Redireciona para a próxima etapa (ex: endereço)
        return redirect(url_for('auth.abrir_conta_endereco')) 
    return render_template('abrir-conta.html') # Mostra a pág. de cadastro

@bp.route('/abrir-conta-endereco', methods=['GET', 'POST'])
def abrir_conta_endereco():
    if request.method == 'POST':
        # Lógica para salvar o endereço...
        return redirect(url_for('auth.abrir_conta_financeiro'))
    return render_template('abrir-conta-endereco.html')

@bp.route('/abrir-conta-dados-financeiros', methods=['GET', 'POST'])
def abrir_conta_financeiro():
    if request.method == 'POST':
        # Lógica para salvar dados financeiros...
        # Redireciona para a próxima etapa (ex: criar senha)
        return redirect(url_for('auth.criar_senha_final')) 
    return render_template('abrir-conta-dados-financeiros.html')

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