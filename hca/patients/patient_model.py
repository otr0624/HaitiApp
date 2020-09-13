from database import db, ma


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))


class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        sqla_session = db.session
