from database import db, ma
from hca.providers.provider_model import Provider, ProviderSchema
from hca.facilities.facility_model import Facility, FacilitySchema
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


class PatientClinicalDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_status_id = db.Column(db.Integer, db.ForeignKey('patient_status.id'))
    patient_urgency_id = db.Column(db.Integer, db.ForeignKey('patient_urgency.id'))
    patient_syndrome_id = db.Column(db.Integer, db.ForeignKey('patient_syndrome.id'))
    syndrome_notes = db.Column(db.Text)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    syndrome = db.relationship('PatientSyndrome', backref='patient_clinical_detail')
    urgency = db.relationship('PatientUrgency', backref='patient_clinical_detail')
    status = db.relationship('PatientStatus', backref='patient_clinical_detail')


class PatientSyndrome(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    syndrome = db.Column(db.String(32))
    syndrome_code = db.Column(db.String(4))


class PatientUrgency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    urgency = db.Column(db.String(32))


class PatientStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32))


class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icd_cat_code = db.Column(db.String(8))
    icd_cat_name = db.Column(db.String(128))
    icd_subcat_code = db.Column(db.String(8))
    icd_subcat_name = db.Column(db.String(128))
    icd_dx_code = db.Column(db.String(8))
    icd_dx_name = db.Column(db.String(128))
    icd_dx_short_name = db.Column(db.String(32))


class PatientContactDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_address_id = db.Column(db.Integer, db.ForeignKey('patient_address.id'))
    patient_contact_notes = db.Column(db.Text())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    patient_address = db.relationship('PatientAddress', backref='patient_contact_detail')

    patient_phone = db.relationship(
        'PatientPhone',
        uselist=True,
        backref='patient_contact_details'
        )

    patient_email = db.relationship(
        'PatientEmail',
        uselist=True,
        backref="patient_contact_details"
        )


class PatientAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_line_1 = db.Column(db.String(128))
    address_line_2 = db.Column(db.String(128))
    city = db.Column(db.String(32))
    state_or_dept = db.Column(db.String(32))
    country = db.Column(db.String(32), default="Haiti")
    notes = db.Column(db.Text())


class PatientPhone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(32), nullable=False)
    owner = db.Column(db.String(32))
    is_primary = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean, default=True)
    has_whatsapp = db.Column(db.Boolean)
    notes = db.Column(db.String(128))
    contact_detail_id = db.Column(db.Integer, db.ForeignKey('patient_contact_detail.id'), nullable=False)


class PatientEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(32), nullable=False)
    owner = db.Column(db.String(32))
    notes = db.Column(db.String(128))
    contact_detail_id = db.Column(db.Integer, db.ForeignKey('patient_contact_detail.id'), nullable=False)


class PassportPriority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passport_priority = db.Column(db.String(32))


# This class includes a list of intermediate documents (birth certs, etc) not directly used for travel
class TravelDocumentDocType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.String(32))


class TravelDocumentEventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(32))


class TravelDocumentEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type_id = db.Column(db.Integer, db.ForeignKey('travel_document_event_type.id'))
    task_owner = db.Column(db.String(32))
    event_date = db.Column(db.Date)
    doc_type_id = db.Column(db.Integer, db.ForeignKey('travel_document_doc_type.id'))
    doc_owner = db.Column(db.String(32))
    notes = db.Column(db.Text())
    travel_detail_id = db.Column(db.Integer, db.ForeignKey('patient_travel_detail.id'), nullable=False)

    event_type = db.relationship('TravelDocumentEventType', backref='travel_document_event')
    doc_type = db.relationship('TravelDocumentDocType', backref='travel_document_event')


class TravelDocumentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(32))


class TravelDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.Text())
    document_type_id = db.Column(db.Integer, db.ForeignKey('travel_document_type.id'))
    country = db.Column(db.String(32))
    owner = db.Column(db.String(32))
    last_name = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date)
    document_number = db.Column(db.String(32))
    issue_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    entries_allowed = db.Column(db.String(32))
    scan_saved = db.Column(db.Boolean)
    travel_detail_id = db.Column(db.Integer, db.ForeignKey('patient_travel_detail.id'), nullable=False)

    document_type = db.relationship('TravelDocumentType', backref='travel_document')


class PatientTravelDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passport_priority_id = db.Column(db.Integer, db.ForeignKey('passport_priority.id'))
    passport_priority_notes = db.Column(db.Text())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    passport_priority = db.relationship('PassportPriority', backref='patient_travel_detail')

    travel_document_event = db.relationship(
        'TravelDocumentEvent',
        uselist=True,
        backref="patient_travel_detail"
    )

    travel_document = db.relationship(
        'TravelDocument',
        uselist=True,
        backref="patient_travel_detail"
    )


class ClinicalEncounterType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))


class ClinicalEncounter(db.Model):
    patient_encounter_detail_id = db.Column(db.Integer, db.ForeignKey('patient_encounter_detail.id'), primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('clinical_encounter_type.id'), primary_key=True)
    date = db.Column(db.Date)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), primary_key=True)
    notes = db.Column(db.Text())

    patient_encounter_detail = db.relationship('PatientEncounterDetail')
    provider = db.relationship('Provider')
    facility = db.relationship('Facility')
    type = db.relationship('ClinicalEncounterType')


class Surgery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), nullable=False)
    surgery_name = db.Column(db.Text)
    rachs_score = db.Column(db.Integer)


class SurgeryEncounter(db.Model):
    patient_encounter_detail_id = db.Column(db.Integer, db.ForeignKey('patient_encounter_detail.id'), primary_key=True)
    surgery_id = db.Column(db.Integer, db.ForeignKey('surgery.id'), primary_key=True)
    date = db.Column(db.Date)
    in_network = db.Column(db.Boolean, default=True)
    lead_surgeon_id = db.Column(db.Integer, db.ForeignKey('provider.id'), primary_key=True)
    surgical_facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), primary_key=True)
    notes = db.Column(db.Text)

    patient_encounter_detail = db.relationship('PatientEncounterDetail')
    surgery = db.relationship('Surgery')
    lead_surgeon = db.relationship('Provider')
    surgical_facility = db.relationship('Facility')


class PatientEncounterDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    clinical_encounter = db.relationship(
        'ClinicalEncounter',
        uselist=True
    )

    surgery_encounter = db.relationship(
        'SurgeryEncounter',
        uselist=True
    )
#
# The 'Schema' definitions have to come after the SQL Alchemy Model definitions
#


class DiagnosisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Diagnosis
        load_instance = True
        sqla_session = db.session


class PatientSyndromeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientSyndrome
        load_instance = True
        sqla_session = db.session


class PatientUrgencySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientUrgency
        load_instance = True
        sqla_session = db.session


class PatientStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientStatus
        load_instance = True
        sqla_session = db.session


class PatientClinicalDetailSchema(ma.SQLAlchemyAutoSchema):

    syndrome = ma.Nested(PatientSyndromeSchema)
    urgency = ma.Nested(PatientUrgencySchema)
    status = ma.Nested(PatientStatusSchema)

    class Meta:
        model = PatientClinicalDetail
        load_instance = True
        sqla_session = db.session
        exclude = ('id', )


class PatientAddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientAddress
        load_instance = True
        sqla_session = db.session


class PatientPhoneSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientPhone
        load_instance = True
        sqla_session = db.session


class PatientEmailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientEmail
        load_instance = True
        sqla_session = db.session


class PatientContactDetailSchema(ma.SQLAlchemyAutoSchema):

    patient_phone = ma.Nested(PatientPhoneSchema, many=True)
    patient_email = ma.Nested(PatientEmailSchema, many=True)
    patient_address = ma.Nested(PatientAddressSchema)

    class Meta:
        model = PatientContactDetail
        load_instance = True
        sqla_session = db.session
        exclude = ('id', )


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


class PassportPrioritySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PassportPriority
        load_instance = True
        sqla_session = db.session


class TravelDocumentEventTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TravelDocumentEventType
        load_instance = True
        sqla_session = db.session


class TravelDocumentDocTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TravelDocumentDocType
        load_instance = True
        sqla_session = db.session


class TravelDocumentEventSchema(ma.SQLAlchemyAutoSchema):

    event_type = ma.Nested(TravelDocumentEventTypeSchema)
    doc_type = ma.Nested(TravelDocumentDocTypeSchema)

    class Meta:
        model = TravelDocumentEvent
        load_instance = True
        sqla_session = db.session


class TravelDocumentTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TravelDocumentDocType
        load_instance = True
        sqla_session = db.session


class TravelDocumentSchema(ma.SQLAlchemyAutoSchema):

    travel_document_type = ma.Nested(TravelDocumentTypeSchema)

    class Meta:
        model = TravelDocument
        load_instance = True
        sqla_session = db.session


class PatientTravelDetailSchema(ma.SQLAlchemyAutoSchema):

    passport_priority = ma.Nested(PassportPrioritySchema)
    travel_document_event = ma.Nested(TravelDocumentEventSchema, many=True)
    travel_document = ma.Nested(TravelDocumentSchema, many=True)

    class Meta:
        model = PatientTravelDetail
        load_instance = True
        sqla_session = db.session
        exclude = ('id', )


class SurgerySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Surgery
        load_instance = True
        sqla_session = db.session


class SurgeryEncounterSchema(ma.SQLAlchemyAutoSchema):

    surgery = ma.Nested(SurgerySchema)
    lead_surgeon = ma.Nested(ProviderSchema)
    surgical_facility = ma.Nested(FacilitySchema)

    class Meta:
        model = SurgeryEncounter
        load_instance = True
        sqla_session = db.session


class ClinicalEncounterTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClinicalEncounterType
        load_instance = True
        sqla_session = db.session


class ClinicalEncounterSchema(ma.SQLAlchemyAutoSchema):

    provider = ma.Nested(ProviderSchema)
    facility = ma.Nested(FacilitySchema)
    type = ma.Nested(ClinicalEncounterTypeSchema)

    class Meta:
        model = ClinicalEncounter
        load_instance = True
        sqla_session = db.session


class PatientEncounterDetailSchema(ma.SQLAlchemyAutoSchema):

    clinical_encounter = ma.Nested(ClinicalEncounterSchema, many=True)
    surgery_encounter = ma.Nested(SurgeryEncounterSchema, many=True)

    class Meta:
        model = PatientEncounterDetail
        load_instance = True
        sqla_session = db.session
        exclude = ('id', )


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
