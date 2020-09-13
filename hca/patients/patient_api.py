from flask import (
    abort
)
from database import db, ma

from hca.patients.patient_model import Patient, PatientSchema


def get_patient_id(id):
    patient = Patient  \
                .query \
                .filter(Patient.id == id) \
                .one_or_none()

    if patient is not None:
        return PatientSchema().dump(patient)

    else:
        abort(404, f'Record not found for Id: {id}')
