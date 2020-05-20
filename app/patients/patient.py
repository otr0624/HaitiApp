from flask import Blueprint, render_template, flash, redirect, url_for
from app.patients.forms import CreatePatientForm

patient_bp = Blueprint('patient_bp', __name__,
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='assets')


@patient_bp.route('/', methods=['GET', 'POST'])
def create_patient():
    form = CreatePatientForm()
    if form.validate_on_submit():
        # Flash message as placeholder until MySQL connection created
        flash('POST request submitted for new patient {} {}'.format(form.pt_first.data, form.pt_last.data))
        return redirect(url_for('index'))
    return render_template('patient.html', title="Patient Dashboard", form=form)
