import connexion

from database import db, ma
import sample_data

import os
import config

from flask_bootstrap import Bootstrap

from hca.patients.patient_views import patients
from hca.providers.provider_views import providers
from hca.facilities.facility_views import facilities


def create_app():

    # Create the Connexion application instance, which wraps
    # the underlying Flask application.
    #
    # Connexion is a framework on top of Flask that automagically 
    # handles HTTP requests defined using OpenAPI (formerly known
    # as Swagger)
    connex = connexion.App(__name__, specification_dir='./api')

    # Read the OpenAPI YAML file to configure the endpoints
    connex.add_api('./reference/OpenAPI.v1.yaml')

    # Setup Flask-Bootstrap
    Bootstrap(connex.app)

    # Configure and initialize the Database and SQLAlchemy
    connex.app.config.from_object(config.DevelopmentConfig)
    db.init_app(connex.app)
    ma.init_app(connex.app)

    connex.app.register_blueprint(patients, url_prefix='/patients')
    connex.app.register_blueprint(providers, url_prefix='/providers')
    connex.app.register_blueprint(facilities, url_prefix='/facilities')
    return connex


if __name__ == '__main__':

    connex = create_app()

    if 'ENV' in os.environ and os.environ['ENV'] == 'prod':
        connex.app.config.from_object('config.ProductionConfig')

    else:
        connex.app.config.from_object('config.DevelopmentConfig')

        # Delete and recreate the development database on launch
        if os.path.exists(connex.app.config['DATABASE_FILENAME']):
            os.remove(connex.app.config['DATABASE_FILENAME'])

        # Setup development database
        with connex.app.app_context():
            # Create non-existent tables
            db.create_all()
            # Populate with sample Patient data
            sample_data.initialize_sample_data(db)

    connex.run()
