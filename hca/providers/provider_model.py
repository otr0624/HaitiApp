from database import db, ma
import uuid


def generate_uuid():
    return uuid.uuid4().hex


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(32),
        default=generate_uuid,
        nullable=False,
        index=True,
        unique=True
        )
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    provider_type = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)


class ProviderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Provider
        load_instance = True
        sqla_session = db.session
