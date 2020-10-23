from database import db, ma
from hca.providers.provider_model import ProviderSchema
from hca.facilities.facility_model import FacilitySchema


class SocialEncounter(db.Model):
    patient_encounter_detail_id = db.Column(db.Integer, db.ForeignKey('patient_encounter_detail.id'), primary_key=True)
    date = db.Column(db.Date)
    notes = db.Column(db.Text())

    patient_encounter_detail = db.relationship('PatientEncounterDetail')


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

    social_encounter = db.relationship(
        'SocialEncounter',
        uselist=True
    )


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


class PatientEncounterDetailSchema(ma.SQLAlchemyAutoSchema):

    clinical_encounter = ma.Nested(ClinicalEncounterSchema, many=True)
    surgery_encounter = ma.Nested(SurgeryEncounterSchema, many=True)
    social_encounter = ma.Nested(SocialEncounterSchema, many=True)

    class Meta:
        model = PatientEncounterDetail
        load_instance = True
        sqla_session = db.session
        exclude = ('id', )