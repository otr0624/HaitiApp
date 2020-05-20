from app import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True, nullable=False)
    last_name = db.Column(db.String(30), index=True, nullable=False)
    status = db.Column(db.String(30), index=True)

    def __repr__(self):
        return '<Patient: {}, {}>'.format(self.last_name, self.first_name)