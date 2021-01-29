from database import db, ma

from hca.patients.submodels.clinical_detail_model import PatientStatus


def get_patient_status_text(text):
    patient_status = (
        PatientStatus
        .query
        .filter(PatientStatus.status == text)
        .one_or_none()
    )

    return patient_status
