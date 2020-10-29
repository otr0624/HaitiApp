from database import db, ma
from hca.providers.provider_model import ProviderSchema
from hca.facilities.facility_model import FacilitySchema


class SocialEncounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    notes = db.Column(db.Text())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)


class ClinicalEncounterType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))


class ClinicalEncounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('clinical_encounter_type.id'), nullable=False)
    date = db.Column(db.Date)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    notes = db.Column(db.Text())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    provider = db.relationship('Provider')
    facility = db.relationship('Facility')
    type = db.relationship('ClinicalEncounterType')


class Surgery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), nullable=False)
    surgery_name = db.Column(db.Text)
    rachs_score = db.Column(db.Integer)


class SurgeryEncounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surgery_id = db.Column(db.Integer, db.ForeignKey('surgery.id'), nullable=False)
    date = db.Column(db.Date)
    in_network = db.Column(db.Boolean, default=True)
    lead_surgeon_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    surgical_facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    notes = db.Column(db.Text)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    # patient = db.relationship('Patient')
    surgery = db.relationship('Surgery')
    lead_surgeon = db.relationship('Provider')
    surgical_facility = db.relationship('Facility')


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


class SocialEncounterSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = SocialEncounter
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
