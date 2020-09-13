from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms_alchemy import ModelForm
from app.patients.patient_model import PatientStatus


class PatientStatusForm(ModelForm, FlaskForm):
    class Meta:
        model = PatientStatus

    submit = SubmitField('Save Changes')
