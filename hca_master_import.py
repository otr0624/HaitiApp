import pandas as pd


def import_hca_master_file(conn):
    df = pd.read_excel("import\hca_master.xlsx")
    df.to_sql('raw_patient_data', conn, if_exists='replace', index=False)
