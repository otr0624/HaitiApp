from database import db, ma

from hca.patients.submodels.travel_detail_model import PassportPriority


def get_passport_priority_text(text):
    passport_priority = (
        PassportPriority
        .query
        .filter(PassportPriority.passport_priority == text)
        .one_or_none()
    )

    return passport_priority
