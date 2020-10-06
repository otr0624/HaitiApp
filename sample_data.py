from hca.patients.patient_model import Patient, PatientClinicalDetail, Diagnosis, PatientDiagnosis
from hca.providers.provider_model import Provider, ProviderCategory
from hca.facilities.facility_model import Facility


def initialize_sample_data(db):

    # #
    # # TESTING ON STARTUP
    # #

    p = Patient()
    p.first_name = "Mike"
    p.last_name = "Smith"
    db.session.add(p)
    db.session.commit()

    pcat1 = ProviderCategory()
    pcat1.category_code = "CARD"
    pcat1.category = "Cardiologist"

    pcat2 = ProviderCategory()
    pcat2.category_code = "SURG"
    pcat2.category = "Surgeon"

    db.session.add_all([pcat1, pcat2])
    db.session.commit()

    pro = Provider()
    pro.first_name = "Hannibal"
    pro.last_name = "Lecter"
    pro.provider_category_id = 1
    pro.facility_id = 1
    pro.notes = "Not presently accepting new patients."
    db.session.add(pro)
    db.session.commit()

    f = Facility()
    f.name = "General Hospital"
    f.facility_type = "Surgical Referral Center"
    f.notes = "This hospital is too expensive."
    db.session.add(f)
    db.session.commit()

    pcd = PatientClinicalDetail()
    pcd.status = 3
    pcd.urgency = 1
    pcd.syndrome = 2
    pcd.syndrome_notes = "These are the notes"
    
    p.clinical_details = pcd

    db.session.add_all([p, pcd])
    db.session.commit()

    d1 = Diagnosis()
    d1.code = "1234"
    d1.diagnosis = "Scraped Knee"

    d2 = Diagnosis()
    d2.code = "5678"
    d2.diagnosis = "Runny Nose"

    pd = PatientDiagnosis()
    pd.diagnosis = d1
    pd.patient = p
    pd.is_primary = True
    pd.is_suspected = False

    pd2 = PatientDiagnosis()
    pd2.diagnosis = d2
    pd2.patient = p
    pd2.is_primary = False
    pd2.is_suspected = True

    db.session.add_all([d1, d2, pd, pd2])
    db.session.commit()

    patient = Patient.query.first()
    print(patient.diagnosis)