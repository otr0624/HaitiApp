from flask import Blueprint, render_template

index_bp = Blueprint('index_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='assets')


@index_bp.route('/')
@index_bp.route('/index')
def index():
    return render_template('index.html', title='Home')
