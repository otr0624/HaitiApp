from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms_alchemy import ModelForm, QuerySelectField
from app.facilities.facility_model import Facility, FacilityCategory


class FacilityCategoryForm(ModelForm, FlaskForm):
    class Meta:
        model = FacilityCategory


class FacilityProfileForm(ModelForm, FlaskForm):
    class Meta:
        model = Facility

    facility_category = QuerySelectField(query_factory=lambda: FacilityCategory.query)

    submit = SubmitField('Create Facility')
    submit_edit = SubmitField('Save Changes')
