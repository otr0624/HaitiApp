from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired


class PatientForm(FlaskForm):
    pt_first = StringField('First Name', validators=[DataRequired()])
    pt_last = StringField('Last Name', validators=[DataRequired()])
    pt_dob = DateField('Date of Birth')
    pt_type = SelectField('Patient Status', choices=[
        ('nochoice', ''),
        ('preop', 'Pre-Op'),
        ('postop', 'Post-Op'),
        ('follow', 'Following'),
        ('undet', 'Undetermined')
    ])
    submit = SubmitField('Create Patient')
