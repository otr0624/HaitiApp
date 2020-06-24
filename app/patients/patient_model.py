from app import db
from app.providers.provider_model import Provider


class PatientStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(30), index=True, nullable=False)
    name = db.Column(db.String(60), index=True, nullable=False)

    def __init__(self, code_name, name=None):
        self.code_name = code_name
        self.name = name or code_name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<PatientStatus: {}, {}>'.format(self.code_name, self.name)


class Patient(db.Model):
    # MAIN TAB
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True, nullable=False, info={'label': 'First Name'})
    last_name = db.Column(db.String(30), index=True, nullable=False, info={'label': 'Last Name'})
    patient_id = db.Column(db.String(10), index=True)
    patient_dob = db.Column(db.Date, info={'label': 'Date of Birth'})
    patient_dob_est = db.Column(db.Boolean, info={'label': 'DOB Estimate?'})
    patient_gender = db.Column(db.String, info={'label': 'Gender'})
    patient_status_id = db.Column(db.Integer, db.ForeignKey('patient_status.id'))
    patient_provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    patient_status = db.relationship(PatientStatus)
    patient_provider = db.relationship(Provider)
    # CLINICAL TAB
    # patient_diagnosis_id = db.Column(db.Integer, db.ForeignKey('patient_status.id'))
    # patient_diagnosis = db.relationship(PatientDiagnosis)
    # patient_urgency_id = db.Column(db.Integer, db.ForeignKey('patient_status.id'))
    # patient_urgency = db.relationship(PatientUrgency)
    # patient_syndrome_id = db.Column(db.Integer, db.ForeignKey('patient_status.id'))
    # patient_syndrome = db.relationship(PatientSyndrome)
    # patient_surgery = ONE TO MANY
    # CONTACT TAB
    # patient_phone = ONE TO MANY
    # patient_address_1 = db.Column(db.String(30), info={'label': 'Address line 1'})
    # patient_address_2 = db.Column(db.String(30), info={'label': 'Address line 2'})
    # patient_address_city = db.Column(db.String(30), info={'label': 'City/Town'})
    # patient_department_id = db.Column(db.Integer, db.ForeignKey('patient_department.id'))
    # patient_department = db.relationship(PatientDepartment)
    # patient_country_id = db.Column(db.Integer, db.ForeignKey('patient_department.id'))
    # patient_country = db.relationship(PatientCountry)
    # TRAVEL TAB
    # patient_passport_priority = db.Column(db.String(15), info={'label': 'Passport Priority'})
    # patient_passport_status_id = db.Column(db.Integer, db.ForeignKey('passport_status.id'))
    # patient_passport_status = db.relationship(PassportStatus)
    # guardian_passport_status_id = db.Column(db.Integer, db.ForeignKey('passport_status.id'))
    # guardian_passport_status = db.relationship(PassportStatus)
    # guardian_passport_identity_last = db.Column(db.String(30), info={'label': 'Last Name'})
    # guardian_passport_identity_first = db.Column(db.String(30), info={'label': 'First Name'})
    # guardian_passport_identity_type_id = db.Column(db.Integer, db.ForeignKey('passport_status.id'))
    # guardian_passport_identity_type = db.relationship(RelationshipType)



    def __init__(self, first_name, last_name, patient_id, patient_status, patient_provider, patient_dob, patient_dob_est, patient_gender):
        # MAIN TAB
        self.first_name = first_name
        self.last_name = last_name
        self.patient_id = patient_id
        self.patient_status = patient_status
        self.patient_provider = patient_provider
        self.patient_dob = patient_dob
        self.patient_dob_est = patient_dob_est
        self.patient_gender = patient_gender
        # CLINICAL TAB
        # CONTACT TAB
        # TRAVEL TAB

    def __repr__(self):
        return '<Patient: {}, {}>'.format(self.last_name, self.first_name)
