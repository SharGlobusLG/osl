import logging
import re

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    """
    1. Add insurance_serial
    2. Copy insurance_number to insurance_serial
    3. Chanhe type of insurance_number to integer
    4. Collect all current insurance_serial (witch was insurance_number before)
    5. Separate char and number to different columns

    The script must be run before Odoo itself deletes the existing column.
    """
    cr.execute('''
        ALTER TABLE osl_hospital_patient
        ADD COLUMN insurance_serial character varying(20)
    ''')
    # _logger.error('ADD COLUMN insurance_serial character varying(20)')

    cr.execute('''
        UPDATE osl_hospital_patient SET 
        insurance_serial = insurance_number,
        insurance_number = NULL
    ''')
    # _logger.error('UPDATE')

    cr.execute('''
        ALTER TABLE osl_hospital_patient
        ALTER COLUMN insurance_number TYPE integer USING insurance_number::integer 
        
    ''')
    # _logger.error('ALTER COLUMN insurance_number TYPE integer USING insurance_number::integer')

    cr.execute("""
        SELECT id, insurance_serial
        FROM osl_hospital_patient
        WHERE insurance_serial IS NOT NULL
          AND insurance_serial != ''
    """)
    # _logger.error('SELECT id, insurance_serial')

    records = cr.fetchall()

    for record_id, policy_number in records:
        # Extract all letters
        serial = ''.join(
            re.findall(r'[^\W\d_]', policy_number, re.UNICODE)
        )

        # Extract all digits
        digits = ''.join(re.findall(r'\d', policy_number))

        number = int(digits) if digits else False

        cr.execute("""
            UPDATE osl_hospital_patient
            SET insurance_serial = %s,
                insurance_number = %s
            WHERE id = %s
        """, (serial, number, record_id))
        # _logger.error('UPDATE osl_hospital_patient')