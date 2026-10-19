from odoo import api, fields, models


class OSLDoctorHistory(models.Model):
    _name = 'osl.hospital.doctor.history'
    _description = 'Історія персональних лікарів'
    _rec_names_search = ['patient_id', 'doctor_id']

    display_name = fields.Char(compute='_compute_display_name', store=False)

    patient_id = fields.Many2one(
        comodel_name='osl.hospital.patient',
        string='Patient',
        required=True,
        ondelete='restrict',
    )

    doctor_id = fields.Many2one(
        comodel_name='osl.hospital.doctor',
        string='Doctor',
        required=True,
        ondelete='restrict',
    )

    appointment_date = fields.Date(
        string='Appointment Date',
        required=True,
        default=fields.Date.today,
    )

    exchange_date = fields.Date(
        string='Doc Exchange Date',
    )

    active = fields.Boolean(
        string='Is Active',
        default=True
    )

    @api.onchange('appointment_date', 'exchange_date')
    def _onchange_appointment_date_exchange_date(self):
        for rec in self:
            if rec.appointment_date and rec.exchange_date and (rec.exchange_date < rec.appointment_date):
                rec.exchange_date = None
                return {
                    'warning': {
                        'title': "Invalid exchange date",
                        'message': "Дата зміни лікаря не може бути раніше ніж дата призначення",
                    }
                }
        return {}

    @api.depends('patient_id', 'doctor_id', 'appointment_date')
    def _compute_display_name(self):
        for record in self:
            displayName = ''
            if record.patient_id:
                displayName += f'{record.patient_id.display_name} - '
            if record.doctor_id:
                displayName += f'{record.doctor_id.display_name}'
            if record.doctor_id.doctor_category_id:
                displayName += f' ({record.doctor_id.doctor_category_id.display_name})'

            record.display_name = displayName + ' ' + str(record.appointment_date)
