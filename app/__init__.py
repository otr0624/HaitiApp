from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

import config

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(config.DevelopmentConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.patients.patient import patient_bp
from app.providers.provider import provider_bp
from app.facilities.facility import facility_bp
from app.general.index import index_bp
from app.general.construction import construction_bp
from app.patients.patient_model import Patient, PatientStatus
from app.providers.provider_model import Provider, ProviderCategory
from app.facilities.facility_model import Facility, FacilityCategory

app.register_blueprint(index_bp, url_prefix='/')
app.register_blueprint(patient_bp, url_prefix='/patients')
app.register_blueprint(provider_bp, url_prefix='/providers')
app.register_blueprint(facility_bp, url_prefix='/facilities')
app.register_blueprint(construction_bp, url_prefix='/')
