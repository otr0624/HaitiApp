from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
# debugging from app import app
from app.facilities.forms import FacilityProfileForm
from app.facilities.facility_model import Facility
from app.general.id_gen import rand_id

facility_bp = Blueprint('facility_bp', __name__,
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='assets')


@facility_bp.route('/')
def view_facility_list():
    facility_list = Facility.query.all()
    return render_template('facilities.html', title="Facility List", facility_list=facility_list)


@facility_bp.route('/new', methods=['GET', 'POST'])
def create_facility():
    form = FacilityProfileForm()
    facility_id = rand_id(4)
    if form.validate_on_submit():
        facility = Facility(
            facility_name=form.facility_name.data,
            facility_category=form.facility_category.data,
            facility_id=facility_id
        )
        db.session.add(facility)
        db.session.commit()
        flash("Facility '{}' successfully created".format(form.facility_name.data))
        return redirect(url_for('facility_bp.view_facility_list'))
    return render_template('new-facility.html', title="Add Facility", form=form)


@facility_bp.route('/delete/<string:facility_id>')
def delete_facility(facility_id):
    try:
        facility = Facility.query.filter_by(facility_id=facility_id).first()
        db.session.delete(facility)
        db.session.commit()
        flash("Facility successfully deleted")
        return view_facility_list()
    except Exception:  # narrow exception to psycopg2.errors.ForeignKeyViolation - need to figure out how
        flash("ERROR: Unable to delete facilities who have providers. "
              "First reassign or delete any providers assigned to this facility, and then try again.", 'error')
        return redirect(url_for('facility_bp.view_facility_list'))

@facility_bp.route('/edit/<string:facility_id>', methods=['GET', 'POST'])
def edit_facility(facility_id):
    facility_obj = Facility.query.filter_by(facility_id=facility_id).first()
    form = FacilityProfileForm(obj=facility_obj)
    if form.validate_on_submit():
        facility_obj.facility_name = form.facility_name.data
        facility_obj.facility_category = form.facility_category.data
        db.session.add(facility_obj)
        db.session.commit()
        flash("Facility '{}' successfully edited".format(form.facility_name.data))
        return redirect(url_for('facility_bp.view_facility_list'))
    return render_template('edit-facility.html',
                           title="Edit Facility",
                           form=form)


@facility_bp.route('/view/<string:facility_id>')
def view_facility(facility_id):
    facility = Facility.query.filter_by(facility_id=facility_id).first()
    return render_template('facility-profile.html',
                           title="View Facility",
                           facility=facility)
