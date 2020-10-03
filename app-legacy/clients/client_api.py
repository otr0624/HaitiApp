from flask import (
    abort
)
from database import db, ma

from app.clients.client_model import Client, ClientSchema


def get_client_id(client_id):
    client = Client  \
                .query \
                .filter(Client.client_id == client_id) \
                .one_or_none()

    if client is not None:
        # Serialize and return
        client_schema = ClientSchema()
        return client_schema.dump(client).data

    else:
        abort(404, f'Record not found for Id: {client_id}')
