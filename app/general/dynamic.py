from flask import Blueprint, render_template

dynamic_bp = Blueprint('dynamic_bp', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='assets')


@dynamic_bp.route('/dynamic')
def dynamic():
    return render_template('dynamic.html')
