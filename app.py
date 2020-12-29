import connexion

from database import db, ma
import sample_data
import data_csv_report, hca_master_import

import os
import config

from flask_bootstrap import Bootstrap

from hca.patients.patient_views import patients
from hca.providers.provider_views import providers
from hca.facilities.facility_views import facilities


# Create the Connexion application instance, which wraps
# the underlying Flask application.
#
# Connexion is a framework on top of Flask that automagically 
# handles HTTP requests defined using OpenAPI (formerly known
# as Swagger)
connex = connexion.FlaskApp(__name__, specification_dir='./api')

# Read the OpenAPI YAML file to configure the endpoints
connex.add_api('./reference/OpenAPI.v1.yaml')

application = connex.app

# Setup Flask-Bootstrap
Bootstrap(connex.app)

# Configure and initialize the Database and SQLAlchemy
connex.app.config.from_object(config.DevelopmentConfig)
db.init_app(connex.app)
ma.init_app(connex.app)

connex.app.register_blueprint(patients, url_prefix='/patients')
connex.app.register_blueprint(providers, url_prefix='/providers')
connex.app.register_blueprint(facilities, url_prefix='/facilities')

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
        # sample_data.initialize_sample_data(db)
        # Export CSV of social encounters due
        # conn = db.engine.connect().connection
        # data_csv_report.export_social_encounters_due(conn)
        # conn.close()
        # Create raw patient data table
        conn = db.engine.connect().connection
        hca_master_import.import_hca_master_file(conn)
        conn.close()
        # Parse data from raw data table and insert into destination patient table
        conn = db.engine.connect().connection
        hca_master_import.parse_master_file_data(conn)
        conn.close()

connex.run()
