from flask import Blueprint

# , render_template, flash, redirect, url_for
# from app import db, ma

providers = Blueprint('providers', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='assets')