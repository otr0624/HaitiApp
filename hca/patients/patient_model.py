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
    status = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.Integer, nullable=False)
    syndrome = db.Column(db.Integer)
    syndrome_notes = db.Column(db.Text)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)


class PatientContactDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_line_1 = db.Column(db.String(128))
    address_line_2 = db.Column(db.String(128))
    address_city = db.Column(db.String(32))
    address_state_or_dept = db.Column(db.String(32))
    address_country = db.Column(db.String(32), default="Haiti")
    address_notes = db.Column(db.Text())

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    patient_phone = db.relationship(
        'PatientPhone',
        uselist=False,
        backref='patient_contact_details'
        )


class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), nullable=False)
    diagnosis = db.Column(db.Text)


class PatientPhone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(32), nullable=False)
    phone_owner = db.Column(db.String(32))
    phone_is_primary = db.Column(db.Boolean)
    phone_is_active = db.Column(db.Boolean)
    phone_notes = db.Column(db.String(128))
    contact_detail_id = db.Column(db.Integer, db.ForeignKey('patient_contact_detail.id'), nullable=False)


#
# The 'Schema' definitions have to come after the SQL Alchemy Model definitions
#


class DiagnosisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Diagnosis
        load_instance = True
        sqla_session = db.session


class PatientClinicalDetailSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = PatientClinicalDetail
        load_instance = True
        sqla_session = db.session
        exclude = ('id', )


class PatientPhoneSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientPhone
        load_instance = True
        sqla_session = db.session


class PatientContactDetailSchema(ma.SQLAlchemyAutoSchema):

    patient_phone = ma.Nested(PatientPhoneSchema)

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


class PatientSchema(ma.SQLAlchemyAutoSchema):

    diagnosis = ma.Nested(PatientDiagnosisSchema, many=True)
    clinical_details = ma.Nested(PatientClinicalDetailSchema)
    contact_details = ma.Nested(PatientContactDetailSchema)
    provider = ma.Nested(PatientProviderSchema, many=True)

    class Meta:
        model = Patient
        load_instance = True
        sqla_session = db.session
