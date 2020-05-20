from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.patients.patient import patient_bp
from app.general.index import index_bp
import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.register_blueprint(patient_bp, url_prefix='/patient')
app.register_blueprint(index_bp, url_prefix='/')

from app.patients.patient_model import Patient

