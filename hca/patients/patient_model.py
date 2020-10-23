from database import db, ma
from hca.providers.provider_model import Provider, ProviderSchema
from hca.facilities.facility_model import Facility, FacilitySchema
from hca.patients.submodels.clinical_detail_model import PatientClinicalDetail, PatientSyndrome, PatientUrgency, \
    PatientStatus, PatientClinicalDetailSchema
from hca.patients.submodels.contact_detail_model import PatientContactDetail, PatientPhone, PatientAddress, \
    PatientEmail, PatientContactDetailSchema
from hca.patients.submodels.travel_detail_model import PassportPriority, TravelDocumentDocType, \
    TravelDocumentEventType, TravelDocumentEvent, TravelDocumentType, TravelDocument, PatientTravelDetail, \
    PatientTravelDetailSchema
from hca.patients.submodels.encounter_detail_model import SocialEncounter, ClinicalEncounterType, ClinicalEncounter, \
    Surgery, SurgeryEncounter, PatientEncounterDetail, PatientEncounterDetailSchema
import uuid


def generate_uuid():
    return uuid.uuid4().hex


class PatientDiagnosis(db.Model):
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis.id'), primary_key=True)
    is_primary = db.Column(db.Boolean)
    is_suspected = db.Column(db.Boolean)
    notes = db.Column(db.Text)

    patient = db.relationship('Patient')
    diagnosis = db.relationship('Diagnosis')


class PatientProvider(db.Model):
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), primary_key=True)
    is_primary = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    notes = db.Column(db.Text)

    patient = db.relationship('Patient')
    provider = db.relationship('Provider')


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(32),
        default=generate_uuid,
        nullable=False,
        index=True,
        unique=True
        )
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date)
    is_date_of_birth_estimate = db.Column(db.Boolean)
    date_of_death = db.Column(db.Date)
    sex = db.Column(db.String(16))

    clinical_details = db.relationship(
        'PatientClinicalDetail',
        uselist=False,
        backref='patient'
        )

    contact_details = db.relationship(
        'PatientContactDetail',
        uselist=False,
        backref='patient'
        )

    travel_details = db.relationship(
        'PatientTravelDetail',
        uselist=False,
        backref='patient'
        )

    encounter_details = db.relationship(
        'PatientEncounterDetail',
        uselist=False,
        backref='patient'
        )

    diagnosis = db.relationship(
        'PatientDiagnosis',
        primaryjoin=id == PatientDiagnosis.patient_id,
        lazy='joined',
        viewonly=True
        )

    provider = db.relationship(
        'PatientProvider',
        primaryjoin=id == PatientProvider.patient_id,
        lazy='joined',
        viewonly=True
        )


class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icd_cat_code = db.Column(db.String(8))
    icd_cat_name = db.Column(db.String(128))
    icd_subcat_code = db.Column(db.String(8))
    icd_subcat_name = db.Column(db.String(128))
    icd_dx_code = db.Column(db.String(8))
    icd_dx_name = db.Column(db.String(128))
    icd_dx_short_name = db.Column(db.String(32))

#
# The 'Schema' definitions have to come after the SQL Alchemy Model definitions
#


class DiagnosisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Diagnosis
        load_instance = True
        sqla_session = db.session


class PatientDiagnosisSchema(ma.SQLAlchemyAutoSchema):

    diagnosis = ma.Nested(DiagnosisSchema)

    class Meta:
        model = PatientDiagnosis
        load_instance = True
        sqla_session = db.session


class PatientProviderSchema(ma.SQLAlchemyAutoSchema):

    provider = ma.Nested(ProviderSchema)

    class Meta:
        model = PatientProvider
        load_instance = True
        sqla_session = db.session


class PatientSchema(ma.SQLAlchemyAutoSchema):

    diagnosis = ma.Nested(PatientDiagnosisSchema, many=True)
    clinical_details = ma.Nested(PatientClinicalDetailSchema)
    contact_details = ma.Nested(PatientContactDetailSchema)
    travel_details = ma.Nested(PatientTravelDetailSchema)
    encounter_details = ma.Nested(PatientEncounterDetailSchema)
    provider = ma.Nested(PatientProviderSchema, many=True)

    class Meta:
        model = Patient
        load_instance = True
        sqla_session = db.session
