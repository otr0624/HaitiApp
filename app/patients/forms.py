from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class PatientProfileForm(FlaskForm):
    pt_first = StringField('First Name', validators=[DataRequired()])
    pt_last = StringField('Last Name', validators=[DataRequired()])
    pt_type = SelectField('Patient Status', choices=[
        ('', ''),
        ('Pre-Op', 'Pre-Op'),
        ('Post-Op', 'Post-Op'),
        ('Following', 'Following'),
        ('Undetermined', 'Undetermined')
    ])
    submit = SubmitField('Create Patient')
    submit_edit = SubmitField('Save Changes')
