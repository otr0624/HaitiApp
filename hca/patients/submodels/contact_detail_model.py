from database import db, ma


class PatientAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_line_1 = db.Column(db.String(128))
    address_line_2 = db.Column(db.String(128))
    city = db.Column(db.String(32))
    state_or_dept = db.Column(db.String(32))
    country = db.Column(db.String(32), default="Haiti")
    notes = db.Column(db.Text())


class PatientPhone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(32), nullable=False)
    owner = db.Column(db.String(32))
    is_primary = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean, default=True)
    has_whatsapp = db.Column(db.Boolean)
    notes = db.Column(db.String(128))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)


class PatientEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(32), nullable=False)
    owner = db.Column(db.String(32))
    notes = db.Column(db.String(128))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)


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
