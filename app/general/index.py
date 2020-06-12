from flask import Blueprint, render_template
from app.patients.patient_model import Patient
from sqlalchemy import func


index_bp = Blueprint('index_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='assets')


@index_bp.route('/')
@index_bp.route('/index')
def index():
    preop_count = Patient.query.filter_by(patient_status_id=2).count()
    postop_count = Patient.query.filter_by(patient_status_id=3).count()
    follow_count = Patient.query.filter_by(patient_status_id=4).count()
    uncat_count = Patient.query.filter_by(patient_status_id=1).count()
    patient_count = len(Patient.query.all())
    return render_template('index.html',
                           title='Home',
                           patient_count=patient_count,
                           preop_count=preop_count,
                           postop_count=postop_count,
                           follow_count=follow_count,
                           uncat_count=uncat_count)
