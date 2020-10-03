from flask import (
    abort
)
from database import db, ma

from hca.facilities.facility_model import (
    Facility,
    FacilitySchema
)

POST_400_MESSAGE = "Do not specify server-generated identifiers ('id', 'uuid' or 'friendly_id') in resource creation requests"


def get_facilities():
    facilities = (
        Facility
        .query
        .order_by(Facility.name)
        .all()
    )
    return FacilitySchema(many=True).dump(facilities)


def post_facilities(body):

    schema = FacilitySchema()
    new_facility = schema.load(body, session=db.session)

    if new_facility.id or new_facility.uuid:
        abort(400, POST_400_MESSAGE)

    db.session.add(new_facility)
    db.session.commit()

    return schema.dump(new_facility), 201


def get_facility_uuid(facility_uuid):
    facility = (
        Facility
        .query
        .filter(Facility.uuid == facility_uuid)
        .one_or_none()
    )

    if facility is None:
        abort(404, f'Record not found for Facility: {facility_uuid}')

    return FacilitySchema().dump(facility)