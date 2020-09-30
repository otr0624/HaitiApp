import connexion
from database import db, ma
import os.path
from flask_bootstrap import Bootstrap

from hca.patients.patient_views import patients
from hca.patients.patient_model import Patient, PatientClinicalDetail, Diagnosis, PatientDiagnosis
from hca.providers.provider_views import providers
from hca.providers.provider_model import Provider

import config


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
    return connex


def setup_database(connex):

    with connex.app.app_context():
        db.create_all()

        # #
        # # TESTING ON STARTUP
        # #

        p = Patient()
        p.first_name = "Mike"
        p.last_name = "Smith"
        db.session.add(p)
        db.session.commit()

        pro = Provider()
        pro.first_name = "Hannibal"
        pro.last_name = "Lecter"
        pro.provider_type = "Specialist"
        pro.notes = "Not presently accepting new patients"
        db.session.add(pro)
        db.session.commit()

        pcd = PatientClinicalDetail()
        pcd.status = 3
        pcd.urgency = 1
        pcd.syndrome = 2
        pcd.syndrome_notes = "These are the notes"
        
        p.clinical_details = pcd

        db.session.add_all([p, pcd])
        db.session.commit()

        d1 = Diagnosis()
        d1.code = "1234"
        d1.diagnosis = "Scraped Knee"

        d2 = Diagnosis()
        d2.code = "5678"
        d2.diagnosis = "Runny Nose"

        pd = PatientDiagnosis()
        pd.diagnosis = d1
        pd.patient = p
        pd.is_primary = True
        pd.is_suspected = False

        pd2 = PatientDiagnosis()
        pd2.diagnosis = d2
        pd2.patient = p
        pd2.is_primary = False
        pd2.is_suspected = True

        db.session.add_all([d1, d2, pd, pd2])
        db.session.commit()

        patient = Patient.query.first()
        print(patient.diagnosis)




if __name__ == '__main__':
    connex = create_app()

    # Because this is just a demonstration we set up the database like this.
    #if not os.path.isfile('app.db'):
    setup_database(connex)

    connex.run(debug=True)
