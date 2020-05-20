from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
from app.patients.forms import CreatePatientForm
from app.patients.patient_model import Patient

patient_bp = Blueprint('patient_bp', __name__,
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='assets')


@patient_bp.route('/')
def view_patient_list():
    return render_template('patients.html', title="Patient List")

@patient_bp.route('/new', methods=['GET', 'POST'])
def create_patient():
    form = CreatePatientForm()
    if form.validate_on_submit():
        patient = Patient(first_name=form.pt_first.data, last_name=form.pt_last.data, status=form.pt_type.data)
        db.session.add(patient)
        db.session.commit()
        flash("Patient '{} {}' added successfully.".format(form.pt_first.data, form.pt_last.data))
        return redirect(url_for('index_bp.index'))
    return render_template('new-patient.html', title="Add Patient", form=form)
