from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms_alchemy import ModelForm, QuerySelectField
from app.providers.provider_model import Provider, ProviderCategory


class ProviderCategoryForm(ModelForm, FlaskForm):
    class Meta:
        model = ProviderCategory


class ProviderProfileForm(ModelForm, FlaskForm):
    class Meta:
        model = Provider

    provider_category = QuerySelectField(query_factory=lambda: ProviderCategory.query)

    submit = SubmitField('Create Provider')
    submit_edit = SubmitField('Save Changes')
