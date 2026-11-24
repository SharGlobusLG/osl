def migrate(cr, version):
    """Find appointments with min scheduled_date and set this date to patient with same id.
    The script is executed after the column has been added."""
    cr.execute('''
        with min_date as (
            select 
	            patient_id,
	            min(scheduled_date) as new_date
            from osl_hospital_appointment
            group by patient_id
        )
        update osl_hospital_patient set 
            first_visit_date = new_date
        from min_date
        where min_date.patient_id = osl_hospital_patient.id
    ''')