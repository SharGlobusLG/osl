def migrate(cr, version):
    """Rename insurance_policy_number TO insurance_number if insurance_policy_number still exists.
    If this script does not execute, the data in the insurance_policy_number column will be lost.
    The script must be executed before Odoo itself deletes the existing column and creates a new, empty one—one that contains no data.
    """
    if column_exists(cr):
        cr.execute('''
            ALTER TABLE osl_hospital_patient
            RENAME COLUMN insurance_policy_number TO insurance_number  
        ''')

def column_exists(cr):
    """Check if insurance_policy_number exists"""
    cr.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'osl_hospital_patient'
              AND column_name = 'insurance_policy_number'
        )
    """)
    return cr.fetchone()[0]