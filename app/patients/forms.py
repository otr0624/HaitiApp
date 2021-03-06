from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, BooleanField
from wtforms_alchemy import ModelForm, QuerySelectField
from app.patients.patient_model import Patient, PatientStatus, PatientDiagnosis
from app.providers.provider_model import Provider


class PatientStatusForm(ModelForm, FlaskForm):
    class Meta:
        model = PatientStatus


class PatientDiagnosisForm(ModelForm, FlaskForm):
    class Meta:
        model = PatientDiagnosis


class PatientProfileForm(ModelForm, FlaskForm):
    class Meta:
        model = Patient

# MAIN TAB
    patient_status = QuerySelectField(query_factory=lambda: PatientStatus.query)
    patient_provider = QuerySelectField(query_factory=lambda: Provider.query)
    patient_gender = RadioField(choices=[('M', 'M'), ('F', 'F'), ('O', 'Other'), ('U', 'Unknown')])
    patient_dob_est = BooleanField('DOB Estimate?')

# CLINICAL TAB
    patient_diagnosis = QuerySelectField(query_factory=lambda: PatientDiagnosis.query, default=None)

# CONTACT TAB

# TRAVEL TAB

    submit_close = SubmitField('Save and Close')
    submit_add = SubmitField('Save and Next Panel')
