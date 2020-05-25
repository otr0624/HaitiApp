from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms_alchemy import ModelForm, QuerySelectField
from app.patients.patient_model import Patient, PatientStatus

class PatientStatusForm(ModelForm,FlaskForm):
    class Meta:
        model=PatientStatus

class PatientProfileForm(ModelForm,FlaskForm):
    class Meta:
        model=Patient

    patient_status=QuerySelectField(query_factory=lambda: PatientStatus.query)

    submit = SubmitField('Create Patient')
    submit_edit = SubmitField('Save Changes')
