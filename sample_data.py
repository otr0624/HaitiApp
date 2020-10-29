from hca.patients.patient_model import Patient, Diagnosis, PatientDiagnosis, PatientProvider, \
    PatientPhone, PatientSyndrome, PatientUrgency, PatientStatus, PatientEmail, PatientAddress, \
    PassportPriority, TravelDocument, TravelDocumentEvent, TravelDocumentType, \
    TravelDocumentEventType, TravelDocumentDocType, ClinicalEncounter, ClinicalEncounterType, \
    Surgery, SurgeryEncounter, SocialEncounter
from hca.providers.provider_model import Provider, ProviderCategory
from hca.facilities.facility_model import Facility, FacilityCategory
from datetime import datetime


def initialize_sample_data(db):
    # #
    # # TESTING ON STARTUP
    # #

    # INITIALIZATION OF ALL DROP-DOWN LIST SAMPLE VALUES

    # # Syndrome list

    s1 = PatientSyndrome()
    s1.syndrome = "Down Syndrome (T21)"
    s1.syndrome_code = "T21"

    s2 = PatientSyndrome()
    s2.syndrome = "Williams Syndrome"
    s2.syndrome_code = "WS"

    s3 = PatientSyndrome()
    s3.syndrome = "Noonan Syndrome"
    s3.syndrome_code = "NS"

    # # Patient Urgency list

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

    # # Patient Status list

    st1 = PatientStatus()
    st1.status = "Pre-Op"

    st2 = PatientStatus()
    st2.status = "Awaiting Diagnosis"

    st3 = PatientStatus()
    st3.status = "Following Non-Surgically"

    st4 = PatientStatus()
    st4.status = "Post-Op"

    # # Passport Priority list

    pp1 = PassportPriority()
    pp1.passport_priority = "ASAP"

    pp2 = PassportPriority()
    pp2.passport_priority = "High"

    pp3 = PassportPriority()
    pp3.passport_priority = "Medium"

    pp4 = PassportPriority()
    pp4.passport_priority = "Low"

    # # Travel Document Type List

    tdt1 = TravelDocumentType()
    tdt1.document_type = "Passport"

    tdt2 = TravelDocumentType()
    tdt2.document_type = "Visa (Visitor)"

    tdt3 = TravelDocumentType()
    tdt3.document_type = "Visa (Transit)"

    tdt4 = TravelDocumentType()
    tdt4.document_type = "Other"

    # # Travel Document Event Type List

    tdet1 = TravelDocumentEventType()
    tdet1.event_type = "Applied"

    tdet2 = TravelDocumentEventType()
    tdet2.event_type = "Completed"

    tdet3 = TravelDocumentEventType()
    tdet3.event_type = "Assigned Task"

    tdet4 = TravelDocumentEventType()
    tdet4.event_type = "Other"

    # # Travel Document Supporting Document Type List

    tddt1 = TravelDocumentDocType()
    tddt1.doc_type = "Birth Certificate"

    tddt2 = TravelDocumentDocType()
    tddt2.doc_type = "Archives Document"

    tddt3 = TravelDocumentDocType()
    tddt3.doc_type = "Electoral Card"

    tddt4 = TravelDocumentDocType()
    tddt4.doc_type = "Court Document"

    tddt5 = TravelDocumentDocType()
    tddt5.doc_type = "Parental Travel Authorization"

    tddt6 = TravelDocumentDocType()
    tddt6.doc_type = "Passport"

    tddt7 = TravelDocumentDocType()
    tddt7.doc_type = "Visa"

    tddt8 = TravelDocumentDocType()
    tddt8.doc_type = "Other"

    # # Surgery Type List

    surg1 = Surgery()
    surg1.code = "3.4"
    surg1.rachs_score = 3
    surg1.surgery_name = "Ventriculomyotomy"

    surg2 = Surgery()
    surg2.code = "3.5"
    surg2.rachs_score = 3
    surg2.surgery_name = "Aortoplasty"

    surg3 = Surgery()
    surg3.code = "3.6"
    surg3.rachs_score = 3
    surg3.surgery_name = "Mitral valvuloplasty or replacement"

    # # Provider Category List

    pcat1 = ProviderCategory()
    pcat1.category_code = "CARD"
    pcat1.category = "Cardiologist"

    pcat2 = ProviderCategory()
    pcat2.category_code = "SURG"
    pcat2.category = "Surgeon"

    # # Facility Category List

    fcat1 = FacilityCategory()
    fcat1.category_code = "SURG"
    fcat1.category = "Surgical Center"

    fcat2 = FacilityCategory()
    fcat2.category_code = "PRIM"
    fcat2.category = "Primary Care Clinic"

    # # Diagnosis List

    d1 = Diagnosis()
    d1.icd_cat_code = "Q"
    d1.icd_cat_name = "Congenital malformations, deformations and chromosomal abnormalities"
    d1.icd_subcat_code = "Q21"
    d1.icd_subcat_name = "Congenital malformations of the circulatory system › Congenital malformations of the cardiac septa"
    d1.icd_dx_code = "0"
    d1.icd_dx_name = "Ventricular septal defect"
    d1.icd_dx_short_name = "VSD"

    d2 = Diagnosis()
    d2.icd_cat_code = "Q"
    d2.icd_cat_name = "Congenital malformations, deformations and chromosomal abnormalities"
    d2.icd_subcat_code = "Q21"
    d2.icd_subcat_name = "Congenital malformations of the circulatory system › Congenital malformations of the cardiac septa"
    d2.icd_dx_code = "1"
    d2.icd_dx_name = "Atrial septal defect"
    d2.icd_dx_short_name = "ASD"

    d3 = Diagnosis()
    d3.icd_cat_code = "Q"
    d3.icd_cat_name = "Congenital malformations, deformations and chromosomal abnormalities"
    d3.icd_subcat_code = "Q21"
    d3.icd_subcat_name = "Congenital malformations of the circulatory system › Congenital malformations of the cardiac septa"
    d3.icd_dx_code = "2"
    d3.icd_dx_name = "Atrioventricular septal defect"
    d3.icd_dx_short_name = "AVSD"

    d4 = Diagnosis()
    d4.icd_cat_code = "Q"
    d4.icd_cat_name = "Congenital malformations, deformations and chromosomal abnormalities"
    d4.icd_subcat_code = "Q21"
    d4.icd_subcat_name = "Congenital malformations of the circulatory system › Congenital malformations of the cardiac septa"
    d4.icd_dx_code = "2"
    d4.icd_dx_name = "Tetralogy of Fallot"
    d4.icd_dx_short_name = "TOF"

    # # Clinical Encounter Type List

    cet1 = ClinicalEncounterType()
    cet1.type = "Outpatient Cardiac"

    cet2 = ClinicalEncounterType()
    cet2.type = "Outpatient Non-Cardiac"

    cet3 = ClinicalEncounterType()
    cet3.type = "Inpatient Admission"

    cet4 = ClinicalEncounterType()
    cet4.type = "Other"

    db.session.add_all([s1, s2, s3, urg1, urg2, urg3, urg4, urg5, st1, st2, st3, st4, pp1, pp2, pp3, pp4, tdt1, tdt2,
                        tdt3, tdt4, tdet1, tdet2, tdet3, tdet4, tddt1, tddt2, tddt3, tddt4, tddt5, tddt6, tddt7, tddt8,
                        pcat1, pcat2, fcat1, fcat2, d1, d2, d3, d4, cet1, cet2, cet3, cet4, surg1, surg2, surg3])
    db.session.commit()

    # INITIALIZATION OF PATIENT OBJECT

    p = Patient()
    p.first_name = "Mike"
    p.last_name = "Smith"
    p.date_of_birth = datetime(2004, 4, 8)
    p.is_date_of_birth_estimate = False
    p.sex = "M"
    db.session.add(p)
    db.session.commit()

    # INITIALIZATION OF PROVIDER OBJECTS

    pro1 = Provider()
    pro1.first_name = "Hannibal"
    pro1.last_name = "Lecter"
    pro1.provider_category_id = 1
    pro1.facility_id = 1
    pro1.notes = "Not presently accepting new patients."

    pro2 = Provider()
    pro2.first_name = "Joe"
    pro2.last_name = "Smith"
    pro2.provider_category_id = 2
    pro2.facility_id = 1
    pro2.notes = "Also does caths."
    db.session.add_all([pro1, pro2])
    db.session.commit()

    # INITIALIZATION OF FACILITY OBJECTS

    f1 = Facility()
    f1.name = "General Hospital"
    f1.notes = "This hospital is too expensive."
    f1.facility_category_id = 1

    f2 = Facility()
    f2.name = "Smalltown Clinic"
    f2.notes = "Basic services only."
    f2.facility_category_id = 2
    db.session.add_all([f1, f2])
    db.session.commit()

    # INITIALIZATION OF PATIENT DATA COLLECTION SUB-TABLES FOR SAMPLE PATIENT

    p.patient_syndrome_id = 1
    p.syndrome_notes = "These are the syndrome notes"
    p.patient_status_id = 2
    p.patient_urgency_id = 2

    p.patient_contact_notes = "This patient usually needs multiple reminders to go to appointments"

    p.passport_priority_notes = "The patient's family can get their own passports"
    p.passport_priority_id = 3

    db.session.add(p)
    db.session.commit()

    # CREATE CONTACT OBJECTS WITHIN CONTACT DETAIL

    pa1 = PatientAddress()
    pa1.address_line_1 = "5 Main Street"
    pa1.address_line_2 = "Apartment 6"
    pa1.city = "Petionville"
    pa1.state_or_dept = "Ouest"
    pa1.notes = "Big blue house on corner"

    p.patient_address = pa1

    pp1 = PatientPhone()
    pp1.phone_number = "4432 5413"
    pp1.owner = "Mother"
    pp1.is_primary = True
    pp1.has_whatsapp = False
    pp1.notes = "Only answers in evenings"

    pp2 = PatientPhone()
    pp2.phone_number = "3545 4567"
    pp2.owner = "Grandmother"
    pp2.is_primary = False
    pp2.has_whatsapp = True
    pp2.notes = "Lives next town over"

    p.patient_phone.extend([pp1, pp2])

    pe1 = PatientEmail()
    pe1.email_address = "fake@email.com"
    pe1.owner = "US Advocate"
    pe1.notes = "Only email if patient unreachable by phone"

    p.patient_email.append(pe1)

    db.session.add_all([p, pa1, pp1, pp2, pe1])
    db.session.commit()

    # CREATE TRAVEL OBJECTS WITHIN TRAVEL DETAIL

    ptd1 = TravelDocument()
    ptd1.country = "USA"
    ptd1.type_id = 2
    ptd1.owner = "Patient"
    ptd1.document_number = "F1234567"
    ptd1.entries_allowed = "Multiple"
    ptd1.issue_date = datetime(2020, 5, 5)
    ptd1.expiration_date = datetime(2025, 5, 4)

    ptd2 = TravelDocument()
    ptd2.country = "Haiti"
    ptd2.type_id = 1
    ptd2.owner = "Mother"
    ptd2.document_number = "512345267"
    ptd2.issue_date = datetime(2017, 1, 3)
    ptd2.expiration_date = datetime(2027, 1, 2)

    p.travel_document.extend([ptd1, ptd2])

    ptde1 = TravelDocumentEvent()
    ptde1.event_type_id = 1
    ptde1.doc_type_id = 3
    ptde1.doc_owner = "Patient"
    ptde1.task_owner = "A1 Paperwork Agency"
    ptde1.notes = "Expect two week turnaround"

    ptde2 = TravelDocumentEvent()
    ptde2.event_type_id = 2
    ptde2.doc_type_id = 2
    ptde2.doc_owner = "Father"
    ptde2.task_owner = "National Archives Office"
    ptde2.notes = "Father will notify when done"

    p.travel_document_event.extend([ptde1, ptde2])

    db.session.add_all([p, ptd1, ptd2, ptde1, ptde2])
    db.session.commit()

    # CREATE CLINICAL OBJECTS WITHIN CLINICAL DETAIL

    psurg1 = SurgeryEncounter()
    psurg1.surgery_id = 1
    psurg1.lead_surgeon_id = 2
    psurg1.surgical_facility_id = 1
    psurg1.date = datetime(2019, 7, 3)
    psurg1.notes = "No complications reported"

    p.surgery_encounter.append(psurg1)

    pclin1 = ClinicalEncounter()
    pclin1.type_id = 1
    pclin1.date = datetime(2020, 10, 1)
    pclin1.facility_id = 2
    pclin1.provider_id = 1
    pclin1.notes = "Routine checkup"

    p.clinical_encounter.append(pclin1)

    db.session.add_all([p, psurg1, pclin1])
    db.session.commit()

    # CREATE DIAGNOSIS OBJECTS WITHIN DIAGNOSIS ARRAY

    pd1 = PatientDiagnosis()
    pd1.diagnosis = d1
    pd1.patient = p
    pd1.is_primary = True
    pd1.is_suspected = False

    pd2 = PatientDiagnosis()
    pd2.diagnosis = d2
    pd2.patient = p
    pd2.is_primary = False
    pd2.is_suspected = True

    db.session.add_all([pd1, pd2])
    db.session.commit()

    # CREATE PROVIDER RELATIONSHIPS

    ppr1 = PatientProvider()
    ppr1.provider_id = 1
    ppr1.patient = p
    ppr1.is_primary = True

    ppr2 = PatientProvider()
    ppr2.provider_id = 2
    ppr2.patient = p
    ppr2.is_primary = False

    db.session.add_all([ppr1, ppr2])
    db.session.commit()

