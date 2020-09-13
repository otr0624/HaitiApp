from flask import Blueprint, render_template
from app.patients.patient_model import Patient
from app.providers.provider_model import Provider
from app.facilities.facility_model import Facility

index_bp = Blueprint('index_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='assets')


@index_bp.route('/')
@index_bp.route('/index')
def index():
    # PATIENT CHART PARAMETERS ("pt" prefix)
    pt_preop = Patient.query.filter_by(patient_status_id=2).count()
    pt_postop = Patient.query.filter_by(patient_status_id=3).count()
    pt_follow = Patient.query.filter_by(patient_status_id=4).count()
    pt_total = len(Patient.query.all())
    pt_all_other = pt_total - (pt_preop + pt_postop + pt_follow)

    # PROVIDER CHART PARAMETERS ("pr" prefix)
    pr_cardiologist = Provider.query.filter_by(provider_category_id=2).count()
    pr_primary_doc_nurse = Provider.query.filter_by(provider_category_id=3).count() + \
                           Provider.query.filter_by(provider_category_id=4).count()
    pr_social_worker = Provider.query.filter_by(provider_category_id=5).count()
    pr_total = len(Provider.query.all())
    pr_all_other = pr_total - (pr_cardiologist + pr_primary_doc_nurse + pr_social_worker)

    # FACILITY CHART PARAMETERS ("fc" prefix)
    fc_hospital = Facility.query.filter_by(facility_category_id=2).count()
    fc_clinic = Facility.query.filter_by(facility_category_id=3).count() + \
                Facility.query.filter_by(facility_category_id=4).count() + \
                Facility.query.filter_by(facility_category_id=4).count()
    fc_surg_site = Facility.query.filter_by(facility_category_id=6).count()
    fc_total = len(Facility.query.all())
    fc_all_other = fc_total - (fc_hospital + fc_clinic + fc_surg_site)

    return render_template('index.html',
                           title='Home',
                           # PATIENT PARAMETERS
                           pt_preop=pt_preop,
                           pt_postop=pt_postop,
                           pt_follow=pt_follow,
                           pt_all_other=pt_all_other,
                           pt_total=pt_total,
                           # PROVIDER PARAMETERS
                           pr_cardiologist=pr_cardiologist,
                           pr_primary_doc_nurse=pr_primary_doc_nurse,
                           pr_social_worker=pr_social_worker,
                           pr_all_other=pr_all_other,
                           pr_total=pr_total,
                           # FACILITY PARAMETERS
                           fc_hospital=fc_hospital,
                           fc_clinic=fc_clinic,
                           fc_surg_site=fc_surg_site,
                           fc_all_other=fc_all_other,
                           fc_total=fc_total)
