import pandas as pd


def import_hca_master_file(conn):
    df = pd.read_excel(r'./resources/hca_master_fake.xlsx')
    df.to_sql('raw_patient_data', conn, if_exists='replace', index=False)


def parse_master_file_data(conn):
    sql_query = pd.read_sql_query('''
        SELECT 
            "ID" AS uuid,
            "Last" AS last_name,
            "First" AS first_name,
            "DOB" AS date_of_birth,
            "Date of Death/Notification" AS date_of_death,
            "Sex" AS sex
        FROM raw_patient_data
    ''', conn)
    sql_query.to_sql('patient', conn, if_exists='replace', index=False)
    print("Patient data successfully imported to database")
