import pandas as pd


def export_social_encounters_due(conn):
    sql_query = pd.read_sql_query('''
        SELECT 
            patient.id, 
            last_name, 
            first_name, 
            sex, 
            MAX(social_encounter.date) as most_recent_encounter_date, 
            social_encounter.next_outreach_due 
        FROM patient 
        INNER JOIN social_encounter ON social_encounter.patient_id = patient.id 
        WHERE social_encounter.next_outreach_due BETWEEN date('now') AND date('now', '+30 day') 
        GROUP BY patient.id
    ''', conn)

    df = pd.DataFrame(sql_query, columns=['patient_id', 'last_name', 'first_name', 'sex', 'most_recent_encounter_date', 'next_outreach_due'])
    df.to_csv('social_encounters_due.csv', index=False, header=True)
    print('Social Encounters Due exported to CSV')
