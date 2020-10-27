from database import db, ma


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