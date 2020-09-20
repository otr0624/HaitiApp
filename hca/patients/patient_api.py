from flask import (
    abort
)
from database import db, ma

from hca.patients.patient_model import (
    Patient,
    PatientSchema,
    Diagnosis,
    DiagnosisSchema
)


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

    if new_patient.id or new_patient.uuid:
        abort(400, "Do not specify 'id' or 'uuid' in Patient creation request")

    db.session.add(new_patient)
    db.session.commit()

    return schema.dump(new_patient), 201


def get_patient_id(uuid):
    patient = Patient  \
                .query \
                .filter(Patient.uuid == uuid) \
                .one_or_none()

    if patient is not None:
        return PatientSchema().dump(patient)
    else:
        abort(404, f'Record not found for Id: {uuid}')


def get_diagnosis():
    diagnosis = (
        Diagnosis
        .query
        .order_by(Diagnosis.code)
        .all()
    )
    return DiagnosisSchema(many=True).dump(diagnosis)
