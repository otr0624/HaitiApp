from database import db, ma


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