from database import db, ma


class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))


class ClientSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Client
        sqla_session = db.session
