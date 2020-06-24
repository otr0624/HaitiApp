from flask import Blueprint, render_template
from app import db
from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, StringField
from wtforms_alchemy import QuerySelectField
from app.providers.provider_model import Provider

dynamic_bp = Blueprint('dynamic_bp', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='assets')


class PatientProviderPairForm(Form):
    """Subform.
    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    patient_name = StringField('Patient Name')
    provider = QuerySelectField(query_factory=lambda: Provider.query)


class MainForm(FlaskForm):
    """Parent form."""

    duos = FieldList(
        FormField(PatientProviderPairForm),
        min_entries=1,
        max_entries=20
    )


class PatientProviderSet(db.Model):
    """Stores patient-provider sets."""
    __tablename__ = 'pp_set'

    id = db.Column(db.Integer, primary_key=True)


class PatientProviderPair(db.Model):
    """Stores pairs within a patient-provider set."""
    __tablename__ = 'duo'

    id = db.Column(db.Integer, primary_key=True)
    pp_set_id = db.Column(db.Integer, db.ForeignKey('pp_set.id'))

    patient_name = db.Column(db.String(100))
    provider_name = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship(Provider)

    # Relationship
    pp_set = db.relationship(
        'PatientProviderSet',
        backref=db.backref('duos', lazy='dynamic', collection_class=list)
    )


@dynamic_bp.route('/dynamic', methods=['GET', 'POST'])
def index():
    form = MainForm()

    if form.validate_on_submit():
        # Create patient-provider set
        new_pp_set = PatientProviderSet()

        db.session.add(new_pp_set)

        for duo in form.duos.data:
            new_duo = PatientProviderPair(**duo)

            # Add to patient-provider set
            new_pp_set.duos.append(new_duo)

        db.session.commit()

    pp_sets = PatientProviderSet.query
    provider_list = Provider.query
    print(provider_list)

    return render_template(
        'dynamic.html',
        form=form,
        pp_sets=pp_sets,
        provider_list=provider_list
    )


@dynamic_bp.route('/<pp_set_id>', methods=['GET'])
def show_pp_set(pp_set_id):
    """Show the details of a patient-provider set."""
    pp_set = PatientProviderSet.query.filter_by(id=pp_set_id).first()

    return render_template(
        'show.html',
        pp_set=pp_set
    )
