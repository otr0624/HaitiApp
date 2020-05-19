from flask import render_template
from app import app
from app.forms import PatientForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='HCA App Home')

@app.route('/newpatient')
def newpatient():
    form = PatientForm()
    return render_template('newpatient.html', title="Create Patient", form=form)
