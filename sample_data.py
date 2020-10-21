from hca.patients.patient_model import Patient, PatientClinicalDetail, Diagnosis, PatientDiagnosis, PatientProvider, \
    PatientContactDetail, PatientPhone, PatientSyndrome, PatientUrgency, PatientStatus, PatientEmail, PatientAddress, \
    PatientTravelDetail, PassportPriority, TravelDocument, TravelDocumentEvent, TravelDocumentType, \
    TravelDocumentEventType, TravelDocumentDocType
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

    st1 = PatientStatus()
    st1.status = "Pre-Op"

    st2 = PatientStatus()
    st2.status = "Awaiting Diagnosis"

    st3 = PatientStatus()
    st3.status = "Following Non-Surgically"

    st4 = PatientStatus()
    st4.status = "Post-Op"

    pp1 = PassportPriority()
    pp1.passport_priority = "ASAP"

    pp2 = PassportPriority()
    pp2.passport_priority = "High"

    pp3 = PassportPriority()
    pp3.passport_priority = "Medium"

    pp4 = PassportPriority()
    pp4.passport_priority = "Low"

    tdt1 = TravelDocumentType()
    tdt1.travel_document_type = "Passport"

    tdt2 = TravelDocumentType()
    tdt2.travel_document_type = "Visa (Visitor)"

    tdt3 = TravelDocumentType()
    tdt3.travel_document_type = "Visa (Transit)"

    tdt4 = TravelDocumentType()
    tdt4.travel_document_type = "Other"

    tdet1 = TravelDocumentEventType()
    tdet1.travel_document_event_type = "Applied"

    tdet2 = TravelDocumentEventType()
    tdet2.travel_document_event_type = "Completed"

    tdet3 = TravelDocumentEventType()
    tdet3.travel_document_event_type = "Assigned Task"

    tdet4 = TravelDocumentEventType()
    tdet4.travel_document_event_type = "Other"

    tddt1 = TravelDocumentDocType()
    tddt1.travel_document_doc_type = "Birth Certificate"

    tddt2 = TravelDocumentDocType()
    tddt2.travel_document_doc_type = "Archives Document"

    tddt3 = TravelDocumentDocType()
    tddt3.travel_document_doc_type = "Electoral Card"

    tddt4 = TravelDocumentDocType()
    tddt4.travel_document_doc_type = "Court Document"

    tddt5 = TravelDocumentDocType()
    tddt5.travel_document_doc_type = "Parental Travel Authorization"

    tddt6 = TravelDocumentDocType()
    tddt6.travel_document_doc_type = "Passport"

    tddt7 = TravelDocumentDocType()
    tddt7.travel_document_doc_type = "Visa"

    tddt8 = TravelDocumentDocType()
    tddt8.travel_document_doc_type = "Other"

    db.session.add_all([s1, s2, s3, urg1, urg2, urg3, urg4, urg5, st1, st2, st3, st4, pp1, pp2, pp3, pp4, tdt1, tdt2,
                        tdt3, tdt4, tdet1, tdet2, tdet3, tdet4, tddt1, tddt2, tddt3, tddt4, tddt5, tddt6, tddt7, tddt8])
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
    pcd.patient_status_id = 2
    pcd.patient_syndrome_id = 1
    pcd.patient_urgency_id = 2
    pcd.syndrome_notes = "These are the notes"

    p.clinical_details = pcd

    pcon = PatientContactDetail()
    pcon.patient_contact_notes = "This patient usually needs multiple reminders to go to appointments"

    p.contact_details = pcon

    ptrav = PatientTravelDetail()
    ptrav.passport_priority_notes = "The patient's family can get their own passports"
    ptrav.passport_priority_id = 3

    p.travel_details = ptrav

    db.session.add_all([p, pcd, pcon, ptrav])
    db.session.commit()

    ptd1 = TravelDocument()
    ptd1.travel_document_country = "USA"
    ptd1.travel_document_type_id = 2
    ptd1.travel_document_owner = "Patient"
    ptd1.travel_document_number = "F1234567"
    ptd1.travel_document_entries = "Multiple"

    ptrav.travel_document.append(ptd1)

    pa1 = PatientAddress()
    pa1.address_line_1 = "5 Main Street"
    pa1.address_line_2 = "Apartment 6"
    pa1.address_city = "Petionville"
    pa1.address_state_or_dept = "Ouest"
    pa1.address_notes = "Big blue house on corner"

    pcon.patient_address = pa1

    pp1 = PatientPhone()
    pp1.phone_number = "4432 5413"
    pp1.phone_owner = "Mother"
    pp1.phone_notes = "Only answers in evenings"

    pp2 = PatientPhone()
    pp2.phone_number = "3545 4567"
    pp2.phone_owner = "Grandmother"
    pp2.phone_notes = "Lives next town over"

    pcon.patient_phone.extend([pp1, pp2])

    pe1 = PatientEmail()
    pe1.email = "fake@email.com"
    pe1.email_owner = "US Advocate"
    pe1.email_notes = "Only email if patient unreachable by phone"

    pcon.patient_email.append(pe1)

    db.session.add_all([pcon, ptrav, ptd1, pa1, pp1, pp2, pe1])
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
