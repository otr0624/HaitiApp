from flask import Blueprint

# , render_template, flash, redirect, url_for
# from app import db, ma

facilities = Blueprint('facilities', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='assets')