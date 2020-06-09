from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
# debugging from app import app
from app.patients.forms import PatientProfileForm
from app.patients.patient_model import Patient, PatientStatus
from app.patients.id_gen import rand_id

patient_bp = Blueprint('patient_bp', __name__,
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='assets')


@patient_bp.route('/')
def view_patient_list():
    patient_list = Patient.query.all()
    return render_template('patients.html', title="Patient List", patient_list=patient_list)


@patient_bp.route('/new', methods=['GET', 'POST'])
def create_patient():
    form = PatientProfileForm()
    patient_id = rand_id(6)
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            patient_status=form.patient_status.data,
            patient_id=patient_id
        )
        db.session.add(patient)
        db.session.commit()
        flash("Patient '{} {}' successfully created".format(form.first_name.data, form.last_name.data))
        return redirect(url_for('patient_bp.view_patient_list'))
    return render_template('new-patient.html', title="Add Patient", form=form)


@patient_bp.route('/delete/<int:_id>')
def delete_patient(_id):
    patient = Patient.query.filter_by(id=_id).first()
    db.session.delete(patient)
    db.session.commit()
    flash("Patient successfully deleted")
    return view_patient_list()


@patient_bp.route('/edit/<int:_id>', methods=['GET', 'POST'])
def edit_patient(_id):

    from flask import request
    patient_obj = db.session.query(Patient).get(_id)
    #debugging app.logger.debug(f"patient to edit is {patient_obj}")
    form = PatientProfileForm(obj=patient_obj)
    if form.validate_on_submit():
        #debugging app.logger.debug(f"last name would be set to {form.last_name.data}, first {form.first_name.data}, stat {form.patient_status.data.id}")
        patient_obj.last_name = form.last_name.data
        patient_obj.first_name = form.first_name.data
        patient_obj.patient_id = form.patient_id
        patient_obj.patient_status = form.patient_status.data
        db.session.add(patient_obj)
        db.session.commit()
        flash("Patient '{} {}' successfully edited".format(form.first_name.data, form.last_name.data))
        return redirect(url_for('patient_bp.view_patient_list'))
    return render_template('edit-patient.html',
                           title="Edit Patient",
                           form=form)
