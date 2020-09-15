from flask import (
    abort
)
from database import db, ma

from hca.patients.patient_model import Patient, PatientSchema


def get_patients():
    patients = (
        Patient
        .query
        .order_by(Patient.last_name)
        .all()
    )
    return PatientSchema(many=True).dump(patients)


def post_patients(body):

    schema = PatientSchema()
    new_patient = schema.load(body, session=db.session)

    db.session.add(new_patient)
    db.session.commit()

    return schema.dump(new_patient), 201


def get_patient_id(id):
    patient = Patient  \
                .query \
                .filter(Patient.id == id) \
                .one_or_none()

    if patient is not None:
        return PatientSchema().dump(patient)
    else:
        abort(404, f'Record not found for Id: {id}')
