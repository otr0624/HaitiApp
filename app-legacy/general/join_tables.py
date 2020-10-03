from sqlalchemy import Table, ForeignKey, Column
from app import db

patient_provider = Table('patient_provider', db.Model.metadata,
                         Column('post_id', ForeignKey('patient.id'), primary_key=True),
                         Column('post_id', ForeignKey('provider.id'), primary_key=True))

