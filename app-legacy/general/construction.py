from flask import Blueprint, render_template

construction_bp = Blueprint('construction_bp', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='assets')


@construction_bp.route('/404')
def construction():
    return render_template('construction.html')
