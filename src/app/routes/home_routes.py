from flask import render_template, Blueprint

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('index.html') 

@bp.route('/faq')
def faq():
    return render_template('faq.html')

@bp.route('/sobre-nos')
def sobre_nos():
    return render_template('sobre-nos.html')
    
@bp.route('/seguranca')
def seguranca():
    return render_template('seguranca.html')

@bp.route('/termos-de-uso')
def termos_de_uso():
    return render_template('termos-de-uso.html')

@bp.route('/politica-de-privacidade')
def politica_de_privacidade():
    return render_template('politica-de-privacidade.html')

@bp.route('/contato')
def contato():
    return render_template('contato.html')