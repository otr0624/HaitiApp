import pandas as pd
import datetime as dt
import hashlib

from hca.patients.patient_model import (
    Patient,
    Diagnosis,
    PatientDiagnosis,
    PatientProvider,
    PatientPhone,
    PatientSyndrome,
    PatientUrgency,
    PatientStatus,
    PatientEmail,
    PatientAddress,
    PassportPriority,
    TravelDocument,
    TravelDocumentEvent,
    TravelDocumentType,
    TravelDocumentEventType,
    TravelDocumentDocType,
    ClinicalEncounter,
    ClinicalEncounterType,
    Surgery,
    SurgeryEncounter,
    SocialEncounter)

from hca.providers.provider_model import (
    Provider,
    ProviderCategory)

from hca.facilities.facility_model import (
    Facility,
    FacilityCategory)


def generate_table_name():
    today = dt.date.today()
    return f'raw_patient_data_{today.year}_{today.month}_{today.day}'


def concat_iterable_as_string(value_list):
    return ' '.join(map(str, value_list)).encode('utf-8')


def hash(s):
    sha_1 = hashlib.sha1(s)
    return sha_1.hexdigest()


def import_master_spreadsheet(db, master_spreadsheet, table_name):

    '''Import and ingest patient records from a raw HCA spreadsheet'''

    # Load the Master HCA spreadsheet into a Pandas DataFrame
    df = pd.read_excel(master_spreadsheet)

    # Concatenate all fields in a single record (row) then generate a 
    # SHA1 hash from the concatenated values. Write this hash to a new
    # column.
    # 
    # This hash value can be used to check if any record has changed
    # since a previous import.
    df['hash'] = pd.Series(
        df.fillna('').values.tolist(), index=df.index).map(
            lambda values: hash(concat_iterable_as_string(values)))

    # Persist the DataFrame into a raw SQL Table
    try:
        conn = db.engine.connect().connection
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    finally:
        conn.close()


def generate_import_sql(table_name):
    return(f'''SELECT
            "Id" AS import_id,
            "hash" AS import_hash,
            "Status" AS status,
            "Last" AS last_name,
            "First" AS first_name,
            "DOB" AS date_of_birth,
            "Sex" AS sex
        FROM {table_name}''')


def process_import(db, table_name):

    #
    # Load the raw import via SQL into a DataFame. This
    # two-pass approach allows us to perform some basic
    # cleanup and preprecessing via SQL prior to importing
    # into the new data model
    #
    try:
        conn = db.engine.connect().connection
        df = pd.read_sql_query(
                generate_import_sql(table_name),
                conn,
                # Which columns to parse as Python datetimes
                parse_dates=('date_of_birth'))
    finally:
        conn.close()

    for record in df.itertuples():
        try:
            process_record(db, record)
        except Exception as e:
            print(e)
            print(record)


def process_record(db, record):

    #
    # record is a NamedTuple where every field corresponds
    # to a column name of the raw input spreadsheet
    #

    # Check to see if this patient record already exists
    patient = (
        Patient
        .query
        .filter(Patient.import_id == record.import_id)
        .one_or_none()
    )

    if patient:
        # This patient record already exists, check import_hash
        # to see if the record has changed at all
        if patient.import_hash == record.import_hash:
            # Nothing to do
            print(f'Skipped: #{record.import_id}'
                  f' {record.first_name} {record.last_name}'
                  f' no changes since last import')
            return
    else:
        patient = Patient()

    patient.import_id = record.import_id
    patient.import_hash = record.import_hash

    patient.first_name = record.first_name
    patient.last_name = record.last_name

    # If the incoming SQL field could not be parsed as a dateime
    # (i.e. null or missing) the dataframe uses the Numpy value 'NaT',
    # which cannot be assigned to as SQLAlchemy db.Date column type.
    #
    # https://stackoverflow.com/a/42103441
    #
    if not pd.isnull(record.date_of_birth):
        patient.date_of_birth = record.date_of_birth

    patient.is_date_of_birth_estimate = False
    patient.sex = record.sex
    db.session.add(patient)

    db.session.commit()
    print(f'Imported: #{record.import_id}'
          f' {record.first_name} {record.last_name}')
