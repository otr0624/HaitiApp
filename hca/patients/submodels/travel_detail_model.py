from database import db, ma


class PassportPriority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passport_priority = db.Column(db.String(32))


# This class includes a list of intermediate documents (birth certs, etc) not directly used for travel
class TravelDocumentDocType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.String(32))


class TravelDocumentEventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(32))


class TravelDocumentEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type_id = db.Column(db.Integer, db.ForeignKey('travel_document_event_type.id'))
    task_owner = db.Column(db.String(32))
    event_date = db.Column(db.Date)
    doc_type_id = db.Column(db.Integer, db.ForeignKey('travel_document_doc_type.id'))
    doc_owner = db.Column(db.String(32))
    notes = db.Column(db.Text())
    travel_detail_id = db.Column(db.Integer, db.ForeignKey('patient_travel_detail.id'), nullable=False)

    event_type = db.relationship('TravelDocumentEventType', backref='travel_document_event')
    doc_type = db.relationship('TravelDocumentDocType', backref='travel_document_event')


class TravelDocumentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(32))


class TravelDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.Text())
    document_type_id = db.Column(db.Integer, db.ForeignKey('travel_document_type.id'))
    country = db.Column(db.String(32))
    owner = db.Column(db.String(32))
    last_name = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date)
    document_number = db.Column(db.String(32))
    issue_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    entries_allowed = db.Column(db.String(32))
    scan_saved = db.Column(db.Boolean)
    travel_detail_id = db.Column(db.Integer, db.ForeignKey('patient_travel_detail.id'), nullable=False)

    document_type = db.relationship('TravelDocumentType', backref='travel_document')


class PatientTravelDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passport_priority_id = db.Column(db.Integer, db.ForeignKey('passport_priority.id'))
    passport_priority_notes = db.Column(db.Text())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    passport_priority = db.relationship('PassportPriority', backref='patient_travel_detail')

    travel_document_event = db.relationship(
        'TravelDocumentEvent',
        uselist=True,
        backref="patient_travel_detail"
    )

    travel_document = db.relationship(
        'TravelDocument',
        uselist=True,
        backref="patient_travel_detail"
    )


class PassportPrioritySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PassportPriority
        load_instance = True
        sqla_session = db.session


class TravelDocumentEventTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TravelDocumentEventType
        load_instance = True
        sqla_session = db.session


class TravelDocumentDocTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TravelDocumentDocType
        load_instance = True
        sqla_session = db.session


class TravelDocumentEventSchema(ma.SQLAlchemyAutoSchema):

    event_type = ma.Nested(TravelDocumentEventTypeSchema)
    doc_type = ma.Nested(TravelDocumentDocTypeSchema)

    class Meta:
        model = TravelDocumentEvent
        load_instance = True
        sqla_session = db.session


class TravelDocumentTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TravelDocumentDocType
        load_instance = True
        sqla_session = db.session


class TravelDocumentSchema(ma.SQLAlchemyAutoSchema):

    travel_document_type = ma.Nested(TravelDocumentTypeSchema)

    class Meta:
        model = TravelDocument
        load_instance = True
        sqla_session = db.session


class PatientTravelDetailSchema(ma.SQLAlchemyAutoSchema):

    passport_priority = ma.Nested(PassportPrioritySchema)
    travel_document_event = ma.Nested(TravelDocumentEventSchema, many=True)
    travel_document = ma.Nested(TravelDocumentSchema, many=True)

    class Meta:
        model = PatientTravelDetail
        load_instance = True
        sqla_session = db.session
        exclude = ('id', )