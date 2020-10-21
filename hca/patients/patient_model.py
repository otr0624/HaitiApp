from database import db, ma
from hca.providers.provider_model import Provider, ProviderSchema
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
    code = db.Column(db.String(32), nullable=False)
    diagnosis = db.Column(db.Text)


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
    address_city = db.Column(db.String(32))
    address_state_or_dept = db.Column(db.String(32))
    address_country = db.Column(db.String(32), default="Haiti")
    address_notes = db.Column(db.Text())


class PatientPhone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(32), nullable=False)
    phone_owner = db.Column(db.String(32))
    phone_is_primary = db.Column(db.Boolean)
    phone_is_active = db.Column(db.Boolean, default=True)
    phone_has_whatsapp = db.Column(db.Boolean)
    phone_notes = db.Column(db.String(128))
    contact_detail_id = db.Column(db.Integer, db.ForeignKey('patient_contact_detail.id'), nullable=False)


class PatientEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), nullable=False)
    email_owner = db.Column(db.String(32))
    email_notes = db.Column(db.String(128))
    contact_detail_id = db.Column(db.Integer, db.ForeignKey('patient_contact_detail.id'), nullable=False)


class PassportPriority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passport_priority = db.Column(db.String(32))


# This class includes a list of intermediate documents (birth certs, etc) not directly used for travel
class TravelDocumentDocType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel_document_doc_type = db.Column(db.String(32))


class TravelDocumentEventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel_document_event_type = db.Column(db.String(32))


class TravelDocumentEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel_document_event_type_id = db.Column(db.Integer, db.ForeignKey('travel_document_event_type.id'))
    travel_document_event_owner = db.Column(db.String(32))
    travel_document_event_date = db.Column(db.Date)
    travel_document_doc_type_id = db.Column(db.Integer, db.ForeignKey('travel_document_doc_type.id'))
    travel_document_doc_owner = db.Column(db.String(32))
    travel_document_event_notes = db.Column(db.Text())
    travel_detail_id = db.Column(db.Integer, db.ForeignKey('patient_travel_detail.id'), nullable=False)

    travel_document_event_type = db.relationship('TravelDocumentEventType', backref='travel_document_event')
    travel_document_doc_type = db.relationship('TravelDocumentDocType', backref='travel_document_event')


class TravelDocumentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel_document_type = db.Column(db.String(32))


class TravelDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel_document_notes = db.Column(db.Text())
    travel_document_type_id = db.Column(db.Integer, db.ForeignKey('travel_document_type.id'))
    travel_document_country = db.Column(db.String(32))
    travel_document_owner = db.Column(db.String(32))
    travel_document_last_name = db.Column(db.String(128))
    travel_document_first_name = db.Column(db.String(128))
    travel_document_dob = db.Column(db.Date)
    travel_document_number = db.Column(db.String(32))
    travel_document_issue_date = db.Column(db.Date)
    travel_document_expiration_date = db.Column(db.Date)
    travel_document_entries = db.Column(db.String(32))
    travel_document_scan_saved = db.Column(db.Boolean)
    travel_detail_id = db.Column(db.Integer, db.ForeignKey('patient_travel_detail.id'), nullable=False)

    travel_document_type = db.relationship('TravelDocumentType', backref='travel_document')


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
        model = PassportPriority
        load_instance = True
        sqla_session = db.session


class TravelDocumentDocTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PassportPriority
        load_instance = True
        sqla_session = db.session


class TravelDocumentEventSchema(ma.SQLAlchemyAutoSchema):

    travel_document_event_type = ma.Nested(TravelDocumentEventTypeSchema)
    travel_document_doc_type = ma.Nested(TravelDocumentDocTypeSchema)

    class Meta:
        model = TravelDocumentEvent
        load_instance = True
        sqla_session = db.session


class TravelDocumentSchema(ma.SQLAlchemyAutoSchema):
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


class PatientSchema(ma.SQLAlchemyAutoSchema):

    diagnosis = ma.Nested(PatientDiagnosisSchema, many=True)
    clinical_details = ma.Nested(PatientClinicalDetailSchema)
    contact_details = ma.Nested(PatientContactDetailSchema)
    travel_details = ma.Nested(PatientTravelDetailSchema)
    provider = ma.Nested(PatientProviderSchema, many=True)

    class Meta:
        model = Patient
        load_instance = True
        sqla_session = db.session
