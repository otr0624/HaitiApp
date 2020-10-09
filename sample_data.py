from hca.patients.patient_model import Patient, PatientClinicalDetail, Diagnosis, PatientDiagnosis, PatientProvider, PatientContactDetail
from hca.providers.provider_model import Provider, ProviderCategory
from hca.facilities.facility_model import Facility, FacilityCategory


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

    fcat1 = FacilityCategory()
    fcat1.category_code = "SURG"
    fcat1.category = "Surgical Center"

    fcat2 = FacilityCategory()
    fcat2.category_code = "PRIM"
    fcat2.category = "Primary Care Clinic"

    db.session.add_all([fcat1, fcat2])
    db.session.commit()

    pro1 = Provider()
    pro1.first_name = "Hannibal"
    pro1.last_name = "Lecter"
    pro1.provider_category_id = 1
    pro1.facility_id = 1
    pro1.notes = "Not presently accepting new patients."
    db.session.add(pro1)
    db.session.commit()

    pro2 = Provider()
    pro2.first_name = "Joe"
    pro2.last_name = "Smith"
    pro2.provider_category_id = 2
    pro2.facility_id = 1
    pro2.notes = "Also does caths."
    db.session.add(pro2)
    db.session.commit()

    f = Facility()
    f.name = "General Hospital"
    f.facility_type = "Surgical Referral Center"
    f.notes = "This hospital is too expensive."
    f.facility_category_id = 1
    db.session.add(f)
    db.session.commit()

    pcd = PatientClinicalDetail()
    pcd.status = 3
    pcd.urgency = 1
    pcd.syndrome = 2
    pcd.syndrome_notes = "These are the notes"
    
    p.clinical_details = pcd

    pcon = PatientContactDetail()
    pcon.address_line_1 = "5 Main Street"
    pcon.address_line_2 = "Apt 2A"
    pcon.address_city = "Port au Prince"
    pcon.address_state_or_dept = "Ouest"
    pcon.address_notes = "Blue house behind church"

    p.contact_details = pcon

    db.session.add_all([p, pcd, pcon])
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

    ppr1 = PatientProvider()
    ppr1.provider_id = 1
    ppr1.patient = p
    ppr1.is_primary = True

    db.session.add_all([d1, d2, pd, pd2, ppr1])
    db.session.commit()

    patient = Patient.query.first()
    print(patient.diagnosis)