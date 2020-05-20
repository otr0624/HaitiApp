from app import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True, nullable=False)
    last_name = db.Column(db.String(30), index=True, nullable=False)
    status = db.Column(db.String(30), index=True)

    def __init__(self, first_name, last_name, status):
        self.first_name = first_name
        self.last_name = last_name
        self.status = status

    def __repr__(self):
        return '<Patient: {}, {}>'.format(self.last_name, self.first_name)
