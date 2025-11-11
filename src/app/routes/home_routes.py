from flask import render_template, Blueprint

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    # Isso assume que seu arquivo está em /templates/index.html
    return render_template('index.html') 

# --- ADICIONE TODAS ESTAS ROTAS ABAIXO ---

@bp.route('/faq')
def faq():
    # Isso assume que você tem /templates/faq.html
    return render_template('faq.html')

@bp.route('/sobre-nos')
def sobre_nos():
    # Isso assume que você tem /templates/sobre-nos.html
    return render_template('sobre-nos.html')
    
@bp.route('/seguranca')
def seguranca():
    # Isso assume que você tem /templates/seguranca.html
    return render_template('seguranca.html')

@bp.route('/termos-de-uso')
def termos_de_uso():
    # Isso assume que você tem /templates/termos-de-uso.html
    return render_template('termos-de-uso.html')

@bp.route('/politica-de-privacidade')
def politica_de_privacidade():
    # Isso assume que você tem /templates/politica-de-privacidade.html
    return render_template('politica-de-privacidade.html')

@bp.route('/contato')
def contato():
    # Isso assume que você tem /templates/contato.html
    return render_template('contato.html')