from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import PatientForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='HCA App Home')


@app.route('/newpatient', methods=['GET', 'POST'])
def newpatient():
    form = PatientForm()
    if form.validate_on_submit():
        flash('Post request submitted for new patient {} {}'.format(form.pt_first.data, form.pt_last.data))
        return redirect(url_for('index'))
    return render_template('newpatient.html', title="Create Patient", form=form)
