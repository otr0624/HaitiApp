from database import db, ma


class PatientContactDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_address_id = db.Column(db.Integer, db.ForeignKey('patient_address.id'))
    patient_contact_notes = db.Column(db.Text())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    patient_address = db.relationship('PatientAddress', backref='patient_contact_detail')

    patient_phone = db.relationship(
        'PatientPhone',
        uselist=True,
        backref='patient_contact_details'
        )

    patient_email = db.relationship(
        'PatientEmail',
        uselist=True,
        backref="patient_contact_details"
        )


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
    contact_detail_id = db.Column(db.Integer, db.ForeignKey('patient_contact_detail.id'), nullable=False)


class PatientEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(32), nullable=False)
    owner = db.Column(db.String(32))
    notes = db.Column(db.String(128))
    contact_detail_id = db.Column(db.Integer, db.ForeignKey('patient_contact_detail.id'), nullable=False)


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


class PatientContactDetailSchema(ma.SQLAlchemyAutoSchema):

    patient_phone = ma.Nested(PatientPhoneSchema, many=True)
    patient_email = ma.Nested(PatientEmailSchema, many=True)
    patient_address = ma.Nested(PatientAddressSchema)

    class Meta:
        model = PatientContactDetail
        load_instance = True
        sqla_session = db.session
        exclude = ('id', )