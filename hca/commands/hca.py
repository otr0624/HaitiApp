import click
import pandas as pd
import datetime as dt
import hashlib
from database import db

from hca.patients.patient_model import *
from hca.patients.submodels.clinical_detail_model import *
from hca.patients.submodels.clinical_detail_api import *
from hca.patients.submodels.travel_detail_api import *
from hca.patients.submodels.contact_detail_model import *
from hca.patients.submodels.encounter_detail_model import *
from hca.patients.submodels.travel_detail_model import *

from hca.providers.provider_model import *

from hca.facilities.facility_model import *

''' Import data from the master HCA patient tracking spreadsheet. Done in multiple steps:
    
    Phase 1: Save XLSX to Database as raw data

    a. Use Pandas read_excel() to load all records into a DataFrame
    b. Enrich DataFrame (i.e. Add hash of each row contents to track modifications)
    c. Write to database via Pandas to_sql()

    Phase 2: Load raw data and build domain models

    d. Load to new DataFrame via read_sql_query(); Cleanup column titles
    e. Loop through every modified record and build domain model
    f. Persist to database
'''


def generate_table_name():
    today = dt.date.today()
    return f'raw_patient_data_{today.year}_{today.month}_{today.day}'


def concat_iterable_as_string(value_list):
    return ' '.join(map(str, value_list)).encode('utf-8')


def hash(s):
    sha_1 = hashlib.sha1(s)
    return sha_1.hexdigest()


def register(app):

    @app.cli.group()
    def hca():
        """Load and manipulate master HCA Spreadsheet"""
        pass

    @hca.command()
    @click.argument('filename', type=click.Path(exists=True))
    def init(filename):

        """Initialize default categories from spreadsheet"""

        # Iterate through all the sheets in the Categories spreadsheet
        with pd.ExcelFile(filename) as xlsx:
            for sheet in xlsx.sheet_names:

                # The sheet name corresponds to the SQLAlchemy model name
                print(f'Loading {sheet}')

                # Get a DataFrame of that sheet
                df = pd.read_excel(xlsx, sheet)

                # Iterate through the DataFrame line-by-line; build a dict
                # for each line to load into the database
                df.apply(lambda x: init_category(sheet, x.to_dict()), axis=1)

    def init_category(category_model_name, record):

        # Get the corresponding name of the Marshmallow serialization schema
        schema_name = f'{category_model_name}Schema'
        print(f'{schema_name} :: {record}')

        # Using reflection we'll create an instance of the schema class
        # See: https://stackoverflow.com/a/22959003
        klass = globals()[schema_name]
        schema = klass()
        new_category_object = schema.load(record, session=db.session)

        db.session.add(new_category_object)
        db.session.commit()

    @hca.command()
    @click.argument('filename', type=click.Path(exists=True))
    @click.option(
        '--refresh',
        required=False,
        is_flag=True,
        help='Force refresh of patient record')
    def load(filename, refresh):

        """Load patient records from master spreadsheet"""

        table = generate_table_name()

        # Load raw data into a single table
        print(f'Loading raw data from {filename} into {table}')
        import_master_spreadsheet(
            db,
            filename,
            table)

        # Process the imported raw data and build
        # the necessary database objects
        process_import(db, table, refresh)

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

        #
        # For clarity:
        #   - Map Column names to Model fields
        #   - Rename columns with whitespace, non-alpha chars to 
        #     make it easy to work with NamedTuple
        #
        return(f'''SELECT
                "Id" AS import_id,
                "hash" AS import_hash,
                "Status" AS patient_status,
                "Last" AS last_name,
                "First" AS first_name,
                "DOB" AS date_of_birth,
                "Sex" AS sex,
                "Diagnosis" AS diagnosis,
                "Diagnosis comments" AS diagnosis_comments,
                "Contact Notes/Issues" AS patient_contact_notes,
                "Urgency" AS patient_urgency,
                "Syndrome status" AS patient_syndrome,
                "PP Priority" AS passport_priority

            FROM {table_name}''')

    def process_import(db, table_name, refresh):

        #
        # Load the raw import via SQL into a DataFame. This
        # two-pass approach allows us to perform some basic
        # cleanup and preprocessing via SQL prior to importing
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
                load_patient(db, record, refresh)
            except Exception as e:
                print(e)
                print(record)

    def load_patient(db, record, refresh):

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
            if not refresh and patient.import_hash == record.import_hash:
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

        patient.patient_contact_notes = record.patient_contact_notes

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

        if not pd.isnull(record.patient_status):
            patient_status = get_patient_status_text(record.patient_status)
            patient.status = patient_status

        if not pd.isnull(record.patient_urgency):
            patient_urgency = get_patient_urgency_text(record.patient_urgency)
            patient.urgency = patient_urgency

        if not pd.isnull(record.patient_syndrome):
            patient_syndrome = get_patient_syndrome_text(record.patient_syndrome)
            patient.syndrome = patient_syndrome

        if not pd.isnull(record.passport_priority):
            print(record.passport_priority)
            passport_priority = get_passport_priority_text(record.passport_priority)
            patient.passport_priority = passport_priority
            print(passport_priority)

        db.session.add(patient)

        db.session.commit()

        #
        # Now that we have the Patient record created, build the related records
        #
        load_diagnosis(db, record, patient)

        print(f'Imported: #{record.import_id}'
              f' {record.first_name} {record.last_name}')

    def load_diagnosis(db, record, patient):

        diagnosis_list = record.diagnosis.split(",")

        for diagnosis in diagnosis_list:
            # Clean leading and trailing whitespace
            diagnosis = diagnosis.strip()

            # Check to see if this patient record already exists
            # patient = (
            #     Patient
            #     .query
            #     .filter(Patient.import_id == record.import_id)
            #     .one_or_none()
            # )


            # print(diagnosis_list)
