import connexion
from database import db, ma
import os.path
from flask_bootstrap import Bootstrap

from app.clients.client_views import clients
from app.clients.client_model import Client

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

    connex.app.register_blueprint(clients, url_prefix='/clients')
    return connex


def setup_database(connex):

    with connex.app.app_context():
        db.create_all()

        c = Client()
        c.first_name = "Mike"
        c.last_name = "Smith"

        db.session.add(c)
        db.session.commit()


if __name__ == '__main__':
    connex = create_app()

    # Because this is just a demonstration we set up the database like this.
    if not os.path.isfile('app.db'):
        setup_database(connex)

    connex.run(debug=True)
