from flask import render_template, Blueprint

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('home/index.html')