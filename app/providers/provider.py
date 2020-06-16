from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
# debugging from app import app
from app.providers.forms import ProviderProfileForm
from app.providers.provider_model import Provider
from app.general.id_gen import rand_id
import psycopg2.errors

provider_bp = Blueprint('provider_bp', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='assets')


@provider_bp.route('/')
def view_provider_list():
    provider_list = Provider.query.all()
    table_id = "provider-list-table"
    return render_template('providers.html', title="Provider List", provider_list=provider_list, table_id=table_id)


@provider_bp.route('/new', methods=['GET', 'POST'])
def create_provider():
    form = ProviderProfileForm()
    provider_id = rand_id(5)
    if form.validate_on_submit():
        provider = Provider(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            provider_category=form.provider_category.data,
            provider_facility=form.provider_facility.data,
            provider_id=provider_id
        )
        db.session.add(provider)
        db.session.commit()
        flash("Provider '{} {}' successfully created".format(form.first_name.data, form.last_name.data))
        return redirect(url_for('provider_bp.view_provider_list'))
    return render_template('new-provider.html', title="Add Provider", form=form)


@provider_bp.route('/delete/<string:provider_id>')
def delete_provider(provider_id):
    try:
        provider = Provider.query.filter_by(provider_id=provider_id).first()
        db.session.delete(provider)
        db.session.commit()
        flash("Provider successfully deleted")
        return view_provider_list()
    except Exception:  # narrow exception to psycopg2.errors.ForeignKeyViolation - need to figure out how
        flash('ERROR: Unable to delete providers who follow patients. '
              'First reassign any patients dependent on this provider, and then try again.')
        return redirect(url_for('provider_bp.view_provider_list'))

@provider_bp.route('/edit/<string:provider_id>', methods=['GET', 'POST'])
def edit_provider(provider_id):
    provider_obj = Provider.query.filter_by(provider_id=provider_id).first()
    form = ProviderProfileForm(obj=provider_obj)
    if form.validate_on_submit():
        provider_obj.last_name = form.last_name.data
        provider_obj.first_name = form.first_name.data
        provider_obj.provider_category = form.provider_category.data
        provider_obj.provider_facility = form.provider_facility.data
        db.session.add(provider_obj)
        db.session.commit()
        flash("Provider '{} {}' successfully edited".format(form.first_name.data, form.last_name.data))
        return redirect(url_for('provider_bp.view_provider_list'))
    return render_template('edit-provider.html',
                           title="Edit Provider",
                           form=form)

@provider_bp.route('/view/<string:provider_id>')
def view_provider(provider_id):
    provider = Provider.query.filter_by(provider_id=provider_id).first()
    return render_template('provider-profile.html',
                           title="View Provider",
                           provider=provider)
