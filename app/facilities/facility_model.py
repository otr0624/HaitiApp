from app import db


class FacilityCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(30), index=True, nullable=False)
    name = db.Column(db.String(60), index=True, nullable=False)

    def __init__(self, code_name, name=None):
        self.code_name = code_name
        self.name = name or code_name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<FacilityCategory: {}, {}>'.format(self.code_name, self.name)


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(30), index=True, nullable=False, info={'label': 'Facility Name'})
    facility_id = db.Column(db.String(10), index=True)
    facility_category_id = db.Column(db.Integer, db.ForeignKey('facility_category.id'))

    facility_category = db.relationship(FacilityCategory)

    def __init__(self, facility_name, facility_id, facility_category):
        self.facility_name = facility_name
        self.facility_id = facility_id
        self.facility_category = facility_category

    def __repr__(self):
        return '<Facility: {}>'.format(self.facility_name)
