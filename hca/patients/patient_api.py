from flask import (
    abort
)
from database import db, ma

from hca.patients.patient_model import (
    Patient,
    PatientSchema,
    Diagnosis,
    DiagnosisSchema,
    PatientDiagnosis,
    PatientDiagnosisSchema
)


POST_400_MESSAGE = "Do not specify server-generated identifiers ('id', 'uuid' or 'friendly_id') in resource creation requests"


def get_diagnosis():
    diagnosis = (
        Diagnosis
        .query
        .order_by(Diagnosis.code)
        .all()
    )
    return DiagnosisSchema(many=True).dump(diagnosis)


def post_diagnosis(body):
    schema = DiagnosisSchema()
    new_diagnosis = schema.load(body, session=db.session)

    if new_diagnosis.id:
        abort(400, POST_400_MESSAGE)

    db.session.add(new_diagnosis)
    db.session.commit()

    return schema.dump(new_diagnosis), 201


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
        abort(400, POST_400_MESSAGE)

    db.session.add(new_patient)
    db.session.commit()

    return schema.dump(new_patient), 201


def get_patient_uuid(patient_uuid):
    patient = (
        Patient
        .query
        .filter(Patient.uuid == patient_uuid)
        .one_or_none()
    )

    if patient is None:
        abort(404, f'Record not found for Patient: {patient_uuid}')

    return PatientSchema().dump(patient)


def post_patient_diagnosis(patient_uuid, diagnosis_id, body):
    patient = (
        Patient
        .query
        .filter(Patient.uuid == patient_uuid)
        .one_or_none()
    )

    diagnosis = (
        Diagnosis
        .query
        .filter(Diagnosis.id == diagnosis_id)
        .one_or_none()
    )

    if patient is None:
        abort(404, f'Record not found for Patient: {patient_uuid}')

    if diagnosis is None:
        abort(404, f'Record not found for Diagnosis: {diagnosis_id}')

    schema = PatientDiagnosisSchema()
    new_patient_diagnosis = schema.load(body, session=db.session)

    new_patient_diagnosis.patient = patient
    new_patient_diagnosis.diagnosis = diagnosis
    db.session.add(new_patient_diagnosis)
    db.session.commit()

    all_patient_diagnosis = (
        PatientDiagnosis
        .query
        .filter(PatientDiagnosis.patient_id == patient.id)
        .order_by(PatientDiagnosis.diagnosis_id)
        .all()
    )

    return PatientDiagnosisSchema(many=True).dump(all_patient_diagnosis), 201
