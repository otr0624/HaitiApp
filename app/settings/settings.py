from flask import Blueprint, render_template


settings_bp = Blueprint('settings_bp', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='assets')


@settings_bp.route('/')
def settings_home():
    mode = "Settings"
    card_title = "Settings Home"
    return render_template('settings-home-base.html', title="Settings",
                           mode=mode, card_title=card_title)
