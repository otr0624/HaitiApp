from database import db, ma
import uuid


def generate_uuid():
    return uuid.uuid4().hex


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(32),
        default=generate_uuid,
        nullable=False,
        index=True,
        unique=True
        )
    name = db.Column(db.String(64))
    facility_category_id = db.Column(db.Integer, db.ForeignKey('facility_category.id'))
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

    facility_category = db.relationship('FacilityCategory', backref='facilities')


class FacilityCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(32))
    category_code = db.Column(db.String(4))


class FacilityCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FacilityCategory
        load_instance = True
        sqla_session = db.session


class FacilitySchema(ma.SQLAlchemyAutoSchema):

    facility_category = ma.Nested(FacilityCategorySchema)

    class Meta:
        model = Facility
        load_instance = True
        sqla_session = db.session
