from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import PatientForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


# @app.route('/patient', methods=['GET', 'POST'])
# def create_patient():
#     form = PatientForm()
#     if form.validate_on_submit():
#         # Flash message as placeholder until MySQL connection created
#         flash('POST request submitted for new patient {} {}'.format(form.pt_first.data, form.pt_last.data))
#         return redirect(url_for('index'))
#     return render_template('patient.html', title="Patient Dashboard", form=form)
