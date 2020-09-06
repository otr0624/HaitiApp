# import connexion
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from flask_migrate import Migrate
# from flask_bootstrap import Bootstrap

# import config

# # Create the Connexion application instance, which wraps
# # the underlying Flask application in `connex.app`
# #
# # Connexion is a framework on top of Flask that automagically 
# # handles HTTP requests defined using OpenAPI (formerly known
# # as Swagger)
# connex = connexion.App(__name__, specification_dir='../api')

# # Read the OpenAPI YAML file to configure the endpoints
# connex.add_api('./reference/OpenAPI.v1.yaml')

# # Initialize and configure the underlying Flask application
# app = connex.app
# Bootstrap(app)
# app.config.from_object(config.DevelopmentConfig)

# # Config and initialize database 
# db = SQLAlchemy(app)
# ma = Marshmallow(app)
# migrate = Migrate(app, db)

# from app.patients.patient import patient_bp
# from app.providers.provider import provider_bp
# from app.facilities.facility import facility_bp
# from app.settings.settings import settings_bp
# from app.general.index import index_bp
# from app.general.construction import construction_bp
# from app.general.dynamic import dynamic_bp
# from app.patients.patient_model import Patient, PatientStatus
# from app.providers.provider_model import Provider, ProviderCategory
# from app.facilities.facility_model import Facility, FacilityCategory

# app.register_blueprint(index_bp, url_prefix='/')
# app.register_blueprint(patient_bp, url_prefix='/patients')
# app.register_blueprint(provider_bp, url_prefix='/providers')
# app.register_blueprint(facility_bp, url_prefix='/facilities')
# app.register_blueprint(construction_bp, url_prefix='/')
# app.register_blueprint(dynamic_bp, url_prefix='/') # temporary workspace for testing dynamic fields
# app.register_blueprint(settings_bp, url_prefix='/settings')
