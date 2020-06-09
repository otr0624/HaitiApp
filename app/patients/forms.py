from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms_alchemy import ModelForm, QuerySelectField
from app.patients.patient_model import Patient, PatientStatus
from app.patients.id_gen import rand_id


class PatientStatusForm(ModelForm, FlaskForm):
    class Meta:
        model = PatientStatus


class PatientProfileForm(ModelForm, FlaskForm):
    class Meta:
        model = Patient

    patient_status = QuerySelectField(query_factory=lambda: PatientStatus.query)
    patient_id = rand_id(6)

    submit = SubmitField('Create Patient')
    submit_edit = SubmitField('Save Changes')
