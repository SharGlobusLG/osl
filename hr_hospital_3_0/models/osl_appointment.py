import logging

from odoo import api, fields, models
from odoo.exceptions import UserError

from ..constants import APPOINTMENT_STATES, COMPLETED

_logger = logging.getLogger(__name__)

class OSLAppointment(models.Model):
    _name = 'osl.hospital.appointment'
    _description = 'Appointment'

    # name = fields.Char()
    # description = fields.Text()

    state = fields.Selection(
        selection=APPOINTMENT_STATES,
        string='Статус візиту'
    )

    scheduled_date = fields.Datetime(
        string='Запланована дата',
        required=True
    )

    actual_date = fields.Datetime(
        string='Фактична дата'
    )

    doctor_id = fields.Many2one(
        string='Doctor',
        comodel_name='osl.hospital.doctor',
    )

    patient_id = fields.Many2one(
        string='Patient',
        comodel_name='osl.hospital.patient',
        required=True,
    )

    summary = fields.Html(
        string='Summary',
    )

    disease_id = fields.Many2one(
        string='Disease',
        comodel_name='osl.hospital.type.disease'
    )

    def write(self, vals):
        if 'state' in vals and vals['state'] == COMPLETED:
            vals['actual_date'] = fields.Datetime.now()
        return super().write(vals)

    def unlink(self):
        if any(rec._origin.state == COMPLETED for rec in self):
            raise UserError(
                "Cannot delete a finished record."
            )
        return super().unlink()

    @api.onchange('actual_date', 'doctor_id')
    def _onchange_scheduled_actual_date_doctor(self):
        for rec in self:
            if rec._origin.state == COMPLETED:
                rec.actual_date = rec._origin.actual_date
                rec.doctor_id = rec._origin.doctor_id
                return {
                    'warning': {
                        'title': "Appointment already done",
                        'message': "Візит вже відбувся.",
                    }
                }
        return {}

    @api.depends('patient_id', 'doctor_id')
    def _compute_display_name(self):
        for record in self:
            displayName = ''
            if record.patient_id:
                displayName += f'{record.patient_id.display_name} - '
            if record.doctor_id:
                displayName += f'{record.doctor_id.display_name} - '

            if record.doctor_id:
                displayName += f'{record.scheduled_date}'

            record.display_name = displayName
