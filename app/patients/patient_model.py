from app import db


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
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True, nullable=False, info={'label': 'First Name'})
    last_name = db.Column(db.String(30), index=True, nullable=False, info={'label': 'Last Name'})
    patient_status_id = db.Column(db.Integer, db.ForeignKey('patient_status.id'))

    patient_status = db.relationship(PatientStatus)

    def __init__(self, first_name, last_name, patient_status):
        self.first_name = first_name
        self.last_name = last_name
        self.patient_status = patient_status

    def __repr__(self):
        return '<Patient: {}, {}>'.format(self.last_name, self.first_name)
