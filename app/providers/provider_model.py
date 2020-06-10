from app import db


class ProviderCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(30), index=True, nullable=False)
    name = db.Column(db.String(60), index=True, nullable=False)

    def __init__(self, code_name, name=None):
        self.code_name = code_name
        self.name = name or code_name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<ProviderCategory: {}, {}>'.format(self.code_name, self.name)


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True, nullable=False, info={'label': 'First Name'})
    last_name = db.Column(db.String(30), index=True, nullable=False, info={'label': 'Last Name'})
    provider_id = db.Column(db.String(10), index=True)
    provider_category_id = db.Column(db.Integer, db.ForeignKey('provider_category.id'))

    provider_category = db.relationship(ProviderCategory)

    def __init__(self, first_name, last_name, provider_id, provider_category):
        self.first_name = first_name
        self.last_name = last_name
        self.provider_id = provider_id
        self.provider_category = provider_category

    def __repr__(self):
        return '<Provider: {}, {}>'.format(self.last_name, self.first_name)
