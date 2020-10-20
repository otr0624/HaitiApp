from hca.patients.patient_model import Patient, PatientClinicalDetail, Diagnosis, PatientDiagnosis, PatientProvider, \
    PatientContactDetail, PatientPhone, PatientSyndrome, PatientUrgency
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

    s1 = PatientSyndrome()
    s1.syndrome = "Down Syndrome (T21)"
    s1.syndrome_code = "T21"

    s2 = PatientSyndrome()
    s2.syndrome = "Williams Syndrome"
    s2.syndrome_code = "WS"

    s3 = PatientSyndrome()
    s3.syndrome = "Noonan Syndrome"
    s3.syndrome_code = "NS"

    urg1 = PatientUrgency()
    urg1.urgency = "ASAP"

    urg2 = PatientUrgency()
    urg2.urgency = "<6 months"

    urg3 = PatientUrgency()
    urg3.urgency = "6-12 months"

    urg4 = PatientUrgency()
    urg4.urgency = "12-24 months"

    urg5 = PatientUrgency()
    urg5.urgency = ">24 months"

    db.session.add_all([s1, s2, s3, urg1, urg2, urg3, urg4, urg5])
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
    pcd.patient_syndrome_id = 1
    pcd.patient_urgency_id = 2
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

    pp1 = PatientPhone()
    pp1.phone_number = "4432 5413"
    pp1.phone_owner = "Mother"
    pp1.phone_notes = "Only answers in evenings"

    pp2 = PatientPhone()
    pp2.phone_number = "3545 4567"
    pp2.phone_owner = "Grandmother"
    pp2.phone_notes = "Lives next town over"

    pcon.patient_phone.extend([pp1, pp2])

    db.session.add_all([pcon, pp1, pp2])
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
