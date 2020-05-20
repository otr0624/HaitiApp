from flask import Flask
from app.patients.patient import patient_bp
from app.general.index import index_bp
import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

app.register_blueprint(patient_bp, url_prefix='/patient')
app.register_blueprint(index_bp, url_prefix='/')
# from app import routes
