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


class FacilityDisplay:
    list_url = url_for('facility_bp.view_facility_list')
    mode = "Facility"
    table_id = "facility-list-table"

    def __init__(self, facility, card_title, edit_url, list_url, mode, facility_list, table_id, form, facility_id,
                 facility_obj):
        self.facility = facility
        self.card_title = card_title
        self.edit_url = edit_url
        self.list_url = list_url
        self.mode = mode
        self.facility_list = facility_list
        self.table_id = table_id
        self.form = form
        self.facility_id = facility_id
        self.facility_obj = facility_obj

    @facility_bp.route('/view/<string:facility_id>')
    def view_facility(self, facility_id):
        self.facility = Facility.query.filter_by(facility_id=self.facility_id).first()
        self.card_title = self.facility.facility_name
        self.edit_url = url_for('facility_bp.edit_facility', facility_id=self.facility.facility_id)
        return render_template('facility-profile.html',
                               title="View Facility",
                               facility=self.facility, card_title=self.card_title, edit_url=self.edit_url,
                               list_url=self.list_url, mode=self.mode)

    @facility_bp.route('/')
    def view_facility_list(self):
        self.facility_list = Facility.query.all()
        return render_template('facilities.html', title="Facility List", facility_list=self.facility_list,
                               table_id=self.table_id)

    @facility_bp.route('/new', methods=['GET', 'POST'])
    def create_facility(self):
        self.form = FacilityProfileForm()
        self.facility_id = rand_id(4)
        if self.form.validate_on_submit():
            facility = Facility(
                facility_name=self.form.facility_name.data,
                facility_category=self.form.facility_category.data,
                facility_id=self.facility_id
            )
            db.session.add(facility)
            db.session.commit()
            flash("Facility '{}' successfully created".format(self.form.facility_name.data))
            return redirect(url_for('facility_bp.view_facility_list'))
        return render_template('new-facility.html', title="Add Facility", form=self.form)

    @facility_bp.route('/delete/<string:facility_id>')
    def delete_facility(self, facility_id):
        try:
            self.facility = Facility.query.filter_by(facility_id=self.facility_id).first()
            db.session.delete(self.facility)
            db.session.commit()
            flash("Facility successfully deleted")
            return self.view_facility_list()
        except Exception:  # narrow exception to psycopg2.errors.ForeignKeyViolation - need to figure out how
            flash('ERROR: Unable to delete facilities that have active providers. '
                  'First reassign or delete any providers assigned to this facility, and then try again.')
            return redirect(url_for('facility_bp.view_facility_list'))

    @facility_bp.route('/edit/<string:facility_id>', methods=['GET', 'POST'])
    def edit_facility(self, facility_id):
        self.facility_obj = Facility.query.filter_by(facility_id=self.facility_id).first()
        self.form = FacilityProfileForm(obj=self.facility_obj)
        if self.form.validate_on_submit():
            self.facility_obj.facility_name = self.form.facility_name.data
            self.facility_obj.facility_category = self.form.facility_category.data
            db.session.add(self.facility_obj)
            db.session.commit()
            flash("Facility '{}' successfully edited".format(self.form.facility_name.data))
            return redirect(url_for('facility_bp.view_facility_list'))
        return render_template('edit-facility.html',
                               title="Edit Facility",
                               form=self.form)
