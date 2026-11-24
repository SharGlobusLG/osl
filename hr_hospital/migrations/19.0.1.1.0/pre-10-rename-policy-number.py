def migrate(cr, version):
    cr.execute('''
        ALTER TABLE osl_hospital_patient
        RENAME COLUMN insurance_policy_number TO insurance_number  
        ''')
