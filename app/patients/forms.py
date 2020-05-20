from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class CreatePatientForm(FlaskForm):
    pt_first = StringField('First Name', validators=[DataRequired()])
    pt_last = StringField('Last Name', validators=[DataRequired()])
    pt_type = SelectField('Patient Status', choices=[
        ('nochoice', ''),
        ('preop', 'Pre-Op'),
        ('postop', 'Post-Op'),
        ('follow', 'Following'),
        ('undet', 'Undetermined')
    ])
    submit = SubmitField('Create Patient')
