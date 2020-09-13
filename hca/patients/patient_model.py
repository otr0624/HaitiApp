from database import db, ma


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date)
    is_date_of_birth_estimate = db.Column(db.Boolean)
    date_of_death = db.Column(db.Date)
    sex = db.Column(db.String(16))

    clinical_details = db.relationship('PatientClinicalDetail', backref='patient')
    diagnosis = db.relationship('Diagnosis', secondary='patient_diagnosis', viewonly=True)


class PatientClinicalDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.Integer, nullable=False)
    syndrome = db.Column(db.Integer)
    syndrome_notes = db.column(db.Text)

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)


class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), nullable=False)
    diagnosis = db.Column(db.Text)

    patients = db.relationship('Patient', secondary='patient_diagnosis', viewonly=True)


class PatientDiagnosis(db.Model):
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis.id'), primary_key=True)
    is_primary = db.Column(db.Boolean)
    is_suspected = db.Column(db.Boolean)
    notes = db.Column(db.Text)

    patient = db.relationship('Patient', backref='patient_diagnosis')
    diagnosis = db.relationship('Diagnosis', backref='patient_diagnosis')


class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        sqla_session = db.session