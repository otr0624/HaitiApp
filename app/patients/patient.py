from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
# debugging from app import app
from app.patients.forms import PatientProfileForm
from app.patients.patient_model import Patient
from app.general.id_gen import rand_id

patient_bp = Blueprint('patient_bp', __name__,
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='assets')


@patient_bp.route('/')
def view_patient_list():
    patient_list = Patient.query.all()
    table_id = "patient-list-table"
    return render_template('patients.html', title="Patient List", patient_list=patient_list, table_id=table_id)


@patient_bp.route('/new', methods=['GET', 'POST'])
def create_patient():
    form = PatientProfileForm()
    patient_id = rand_id(6)
    activity = "Create"
    card_title = "Create a Patient"
    list_url = url_for('patient_bp.view_patient_list')
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            patient_status=form.patient_status.data,
            patient_provider=form.patient_provider.data,
            patient_id=patient_id
        )
        db.session.add(patient)
        db.session.commit()
        flash("Patient '{} {}' successfully created".format(form.first_name.data, form.last_name.data))
        return redirect(url_for('patient_bp.view_patient_list'))
    return render_template('patient_form/main.html', title="Add Patient", form=form, activity=activity,
                           list_url=list_url, card_title=card_title)


@patient_bp.route('/delete/<string:patient_id>')
def delete_patient(patient_id):
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    db.session.delete(patient)
    db.session.commit()
    flash("Patient successfully deleted")
    return view_patient_list()


@patient_bp.route('/edit/<string:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient_obj = Patient.query.filter_by(patient_id=patient_id).first()
    # debugging app.logger.debug(f"patient to edit is {patient_obj}")
    activity = "Edit"
    card_title = "Edit a Patient"
    list_url = url_for('patient_bp.view_patient_list')
    form = PatientProfileForm(obj=patient_obj)
    if form.validate_on_submit():
        # debugging app.logger.debug(f"last name would be set to {form.last_name.data}, first {form.first_name.data}, stat {form.patient_status.data.id}")
        patient_obj.last_name = form.last_name.data
        patient_obj.first_name = form.first_name.data
        patient_obj.patient_status = form.patient_status.data
        patient_obj.patient_provider = form.patient_provider.data
        db.session.add(patient_obj)
        db.session.commit()
        flash("Patient '{} {}' successfully edited".format(form.first_name.data, form.last_name.data))
        return redirect(url_for('patient_bp.view_patient_list'))
    return render_template('patient_form/main.html',
                           title="Edit Patient",
                           form=form, activity=activity, list_url=list_url, card_title=card_title)


@patient_bp.route('/view/<string:patient_id>')
def view_patient(patient_id):
    active_page = 'main'
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    card_title = patient.last_name + ", " + patient.first_name + " (" + patient.patient_id + ")"
    edit_url = url_for('patient_bp.edit_patient', patient_id=patient.patient_id)
    list_url = url_for('patient_bp.view_patient_list')
    mode = "Patient"
    activity = "View"
    return render_template('patient_profile/main.html',
                           title="View Patient",
                           patient=patient,
                           active_page=active_page, card_title=card_title, edit_url=edit_url, list_url=list_url,
                           mode=mode, activity=activity)


@patient_bp.route('/view/<string:patient_id>/clinical')
def view_patient_clinical(patient_id):
    active_page = 'clinical'
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    card_title = patient.last_name + ", " + patient.first_name + " (" + patient.patient_id + ")"
    edit_url = url_for('patient_bp.edit_patient', patient_id=patient.patient_id)
    list_url = url_for('patient_bp.view_patient_list')
    mode = "Patient"
    activity = "View"
    return render_template('patient_profile/clinical.html',
                           title="View Patient",
                           patient=patient,
                           active_page=active_page, card_title=card_title, edit_url=edit_url, list_url=list_url,
                           mode=mode, activity=activity)


@patient_bp.route('/view/<string:patient_id>/contact')
def view_patient_contact(patient_id):
    active_page = 'contact'
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    card_title = patient.last_name + ", " + patient.first_name + " (" + patient.patient_id + ")"
    edit_url = url_for('patient_bp.edit_patient', patient_id=patient.patient_id)
    list_url = url_for('patient_bp.view_patient_list')
    mode = "Patient"
    activity = "View"
    return render_template('patient_profile/contact.html',
                           title="View Patient",
                           patient=patient,
                           active_page=active_page, card_title=card_title, edit_url=edit_url, list_url=list_url,
                           mode=mode, activity=activity)


@patient_bp.route('/view/<string:patient_id>/travel')
def view_patient_travel(patient_id):
    active_page = 'travel'
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    card_title = patient.last_name + ", " + patient.first_name + " (" + patient.patient_id + ")"
    edit_url = url_for('patient_bp.edit_patient', patient_id=patient.patient_id)
    list_url = url_for('patient_bp.view_patient_list')
    mode = "Patient"
    activity = "View"
    return render_template('patient_profile/travel.html',
                           title="View Patient",
                           patient=patient,
                           active_page=active_page, card_title=card_title, edit_url=edit_url, list_url=list_url,
                           mode=mode, activity=activity)


@patient_bp.route('/view/<string:patient_id>/history')
def view_patient_history(patient_id):
    active_page = 'history'
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    card_title = patient.last_name + ", " + patient.first_name + " (" + patient.patient_id + ")"
    edit_url = url_for('patient_bp.edit_patient', patient_id=patient.patient_id)
    list_url = url_for('patient_bp.view_patient_list')
    mode = "Patient"
    activity = "View"
    return render_template('patient_profile/history.html',
                           title="View Patient",
                           patient=patient,
                           active_page=active_page, card_title=card_title, edit_url=edit_url, list_url=list_url,
                           mode=mode, activity=activity)


@patient_bp.route('/view/<string:patient_id>/files')
def view_patient_files(patient_id):
    active_page = 'files'
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    card_title = patient.last_name + ", " + patient.first_name + " (" + patient.patient_id + ")"
    edit_url = url_for('patient_bp.edit_patient', patient_id=patient.patient_id)
    list_url = url_for('patient_bp.view_patient_list')
    mode = "Patient"
    activity = "View"
    return render_template('patient_profile/files.html',
                           title="View Patient",
                           patient=patient,
                           active_page=active_page, card_title=card_title, edit_url=edit_url, list_url=list_url,
                           mode=mode, activity=activity)
