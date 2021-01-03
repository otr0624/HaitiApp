from database import db, ma
from hca.providers.provider_model import Provider, ProviderSchema
from hca.facilities.facility_model import Facility, FacilitySchema
from hca.patients.submodels.clinical_detail_model import PatientSyndrome, PatientUrgency, \
    PatientStatus, PatientSyndromeSchema, PatientStatusSchema, PatientUrgencySchema
from hca.patients.submodels.contact_detail_model import PatientPhone, PatientAddress, \
    PatientEmail, PatientAddressSchema, PatientPhoneSchema, PatientEmailSchema
from hca.patients.submodels.travel_detail_model import PassportPriority, TravelDocumentDocType, \
    TravelDocumentEventType, TravelDocumentEvent, TravelDocumentType, TravelDocument, \
    PassportPrioritySchema, TravelDocumentSchema, TravelDocumentEventSchema
from hca.patients.submodels.encounter_detail_model import SocialEncounter, ClinicalEncounterType, ClinicalEncounter, \
    Surgery, SurgeryEncounter, ClinicalEncounterSchema, SurgeryEncounterSchema, SocialEncounterSchema
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

    #
    # For records imported from the legacy HCA master spreadsheet,
    # import_id is the Id of the incoming record. May (eventually)
    # be blank when system is fully migrated
    #
    import_id = db.Column(db.Integer)

    #
    # For records imported from the legacy HCA master spreadsheet,
    # import_hash is SHA1 hash of the full incoming record. 
    # 
    # Since the legacy spreadsheet is one patient record per line,
    # we use this hash to determine if any fields have changed since
    # the last import.
    #
    import_hash = db.Column(db.String(64))

    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date)
    is_date_of_birth_estimate = db.Column(db.Boolean)
    date_of_death = db.Column(db.Date)
    sex = db.Column(db.String(16))
    patient_syndrome_id = db.Column(db.Integer, db.ForeignKey('patient_syndrome.id'))
    syndrome_notes = db.Column(db.Text)
    patient_status_id = db.Column(db.Integer, db.ForeignKey('patient_status.id'))
    patient_urgency_id = db.Column(db.Integer, db.ForeignKey('patient_urgency.id'))
    patient_address_id = db.Column(db.Integer, db.ForeignKey('patient_address.id'))
    patient_contact_notes = db.Column(db.Text())
    passport_priority_id = db.Column(db.Integer, db.ForeignKey('passport_priority.id'))
    passport_priority_notes = db.Column(db.Text())
    failed_outreach_count = db.Column(db.Integer)

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

    patient_phone = db.relationship(
        'PatientPhone',
        uselist=True,
        backref='patient'
        )

    patient_email = db.relationship(
        'PatientEmail',
        uselist=True,
        backref="patient"
        )

    clinical_encounter = db.relationship(
        'ClinicalEncounter',
        uselist=True,
        backref="patient"
    )

    surgery_encounter = db.relationship(
        'SurgeryEncounter',
        uselist=True,
        backref="patient"
    )

    social_encounter = db.relationship(
        'SocialEncounter',
        uselist=True,
        backref="patient"
    )

    travel_document_event = db.relationship(
        'TravelDocumentEvent',
        uselist=True,
        backref="patient"
    )

    travel_document = db.relationship(
        'TravelDocument',
        uselist=True,
        backref="patient"
    )

    syndrome = db.relationship('PatientSyndrome', backref='patient')
    status = db.relationship('PatientStatus', backref='patient')
    urgency = db.relationship('PatientUrgency', backref='patient')
    patient_address = db.relationship('PatientAddress', backref='patient')
    passport_priority = db.relationship('PassportPriority', backref='patient')


class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    depth = db.Column(db.Integer)
    icd_section_name = db.Column(db.String(32))
    icd_section_desc = db.Column(db.Text())
    icd_diagnosis_name = db.Column(db.String(32))
    icd_diagnosis_desc = db.Column(db.Text())


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
    provider = ma.Nested(PatientProviderSchema, many=True)
    syndrome = ma.Nested(PatientSyndromeSchema)
    urgency = ma.Nested(PatientUrgencySchema)
    status = ma.Nested(PatientStatusSchema)
    patient_address = ma.Nested(PatientAddressSchema)
    patient_phone = ma.Nested(PatientPhoneSchema, many=True)
    patient_email = ma.Nested(PatientEmailSchema, many=True)
    clinical_encounter = ma.Nested(ClinicalEncounterSchema, many=True)
    surgery_encounter = ma.Nested(SurgeryEncounterSchema, many=True)
    social_encounter = ma.Nested(SocialEncounterSchema, many=True)
    passport_priority = ma.Nested(PassportPrioritySchema)
    travel_document_event = ma.Nested(TravelDocumentEventSchema, many=True)
    travel_document = ma.Nested(TravelDocumentSchema, many=True)

    class Meta:
        model = Patient
        load_instance = True
        sqla_session = db.session
