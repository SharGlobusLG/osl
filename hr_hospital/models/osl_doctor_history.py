from odoo import api, fields, models
from odoo.exceptions import ValidationError


class OSLDoctorHistory(models.Model):
    """ History of changes to the doctor assigned to a patient.
    """
    _name = 'osl.hospital.doctor.history'
    _description = 'Personal Doctors History'
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

    set_date = fields.Date(
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

    @api.onchange('set_date', 'exchange_date')
    def _onchange_set_date_exchange_date(self):
        """The exchange date cannot be earlier than the assignment date.
        """
        for rec in self:
            if rec.set_date and rec.exchange_date and (rec.exchange_date < rec.set_date):
                rec.exchange_date = None
                return {
                    'warning': {
                        'title': self.env._("Invalid exchange date"),
                        'message': self.env._("Doctor's exchange dade can't before set date"),
                    }
                }
        return {}

    @api.depends('patient_id', 'doctor_id', 'set_date')
    def _compute_display_name(self):
        """The display name is composed of reference fields and a date.
        :return: Text with display name.
        """
        for record in self:
            displayName = ''
            if record.patient_id:
                displayName += f'{record.patient_id.display_name} - '
            if record.doctor_id:
                displayName += f'{record.doctor_id.display_name}'
            if record.doctor_id.doctor_category_id:
                displayName += f' ({record.doctor_id.doctor_category_id.display_name})'

            record.display_name = displayName + ' ' + str(record.set_date)

    @api.constrains('set_date', 'exchange_date')
    def _check_parent_recursion(self):
        """ The doctor exchange date must always be later than the set date.
        """
        for rec in self:
            if rec.set_date and rec.exchange_date and (rec.exchange_date < rec.set_date):
                raise ValidationError(
                    self.env._("Doctor's exchange dade can't before set date")
                )
