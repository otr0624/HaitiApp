from flask import (
    abort
)
from database import db, ma

from hca.providers.provider_model import (
    Provider,
    ProviderSchema
)

POST_400_MESSAGE = "Do not specify server-generated identifiers ('id', 'uuid' or 'friendly_id') in resource creation requests"


def get_providers():
    providers = (
        Provider
        .query
        .order_by(Provider.last_name)
        .all()
    )
    return ProviderSchema(many=True).dump(providers)


def post_providers(body):

    schema = ProviderSchema()
    new_provider = schema.load(body, session=db.session)

    if new_provider.id or new_provider.uuid:
        abort(400, POST_400_MESSAGE)

    db.session.add(new_provider)
    db.session.commit()

    return schema.dump(new_provider), 201


def get_provider_uuid(provider_uuid):
    provider = (
        Provider
        .query
        .filter(Provider.uuid == provider_uuid)
        .one_or_none()
    )

    if provider is None:
        abort(404, f'Record not found for Provider: {provider_uuid}')

    return ProviderSchema().dump(provider)
