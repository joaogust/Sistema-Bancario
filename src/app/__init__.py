from flask import Flask
from config import Config
from . import db

# --- FUNÇÃO DO FILTRO ---
def format_currency(value):
    """
    Formata um número decimal para o padrão monetário brasileiro.
    Ex: 1200.50 -> 1.200,50
    """
    try:
        if value is None:
            return "0,00"
        # Formata com vírgula para milhar e ponto para decimal (padrão US)
        # Ex: 1,200.50
        us_format = "{:,.2f}".format(value)
        # Troca a vírgula por um placeholder, o ponto por vírgula, e o placeholder por ponto
        return us_format.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return value

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    # --- REGISTRO DO FILTRO (ESSENCIAL) ---
    # Isso ensina ao HTML o que é 'format_currency'
    app.jinja_env.filters['format_currency'] = format_currency
    
    # Registra os blueprints
    from .routes import home_routes
    app.register_blueprint(home_routes.bp)

    from .routes import auth_routes
    app.register_blueprint(auth_routes.bp)

    from .routes import conta_routes
    app.register_blueprint(conta_routes.bp)

    return app