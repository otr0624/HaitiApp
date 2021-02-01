from database import db, ma

from hca.patients.submodels.clinical_detail_model import PatientStatus, PatientUrgency, PatientSyndrome


def get_patient_status_text(text):
    patient_status = (
        PatientStatus
        .query
        .filter(PatientStatus.status == text)
        .one_or_none()
    )

    return patient_status


def get_patient_urgency_text(text):
    patient_urgency = (
        PatientUrgency
        .query
        .filter(PatientUrgency.urgency == text)
        .one_or_none()
    )

    return patient_urgency


def get_patient_syndrome_text(text):
    patient_syndrome = (
        PatientSyndrome
        .query
        .filter(PatientSyndrome.syndrome == text)
        .one_or_none()
    )

    return patient_syndrome
