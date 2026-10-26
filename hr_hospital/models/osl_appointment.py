import logging

from odoo import api, fields, models
from odoo.exceptions import UserError


from ..constants import APPOINTMENT_STATES, COMPLETED, SCHEDULED

_logger = logging.getLogger(__name__)

APPOINTMENT_DONE = 'Appointment already done'

class OSLAppointment(models.Model):
    _name = 'osl.hospital.appointment'
    _description = 'Appointment'

    # name = fields.Char()
    # description = fields.Text()

    state = fields.Selection(
        selection=APPOINTMENT_STATES,
        string='Статус візиту',
        default=SCHEDULED,
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
        comodel_name='osl.hospital.type.disease',
        ondelete='set null',
    )

    count_same_disease = fields.Integer(
        stored=False,
        compute='_compute_count_same_disease'
    )

    def write(self, vals):
        for rec in self:
            if rec._origin.state == COMPLETED and ('scheduled_date' in vals or 'doctor_id' in vals):
                raise UserError(self.env._(APPOINTMENT_DONE))

        if 'state' in vals and vals['state'] == COMPLETED:
            if self._origin.state == COMPLETED and ('scheduled_date' in vals or 'doctor_id' in vals):
                vals['actual_date'] = fields.Datetime.now()

        return super().write(vals)

    def unlink(self):
        if any(rec._origin.state == COMPLETED for rec in self):
            if self.env.context.get('_force_unlink'):
                return super().unlink()
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
                        'title': APPOINTMENT_DONE,
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

    def show_disease_like_this(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Така сама хвороба',
            'res_model': 'osl.hospital.appointment',
            'view_mode': 'list',
            'domain': [("disease_id","=",self.disease_id.id)],
            'target': 'current',
        }

    @api.depends('disease_id')
    def _compute_count_same_disease(self):
        self.ensure_one()
        for rec in self:
            rec.count_same_disease = self.env['osl.hospital.appointment'].search_count([('disease_id', '=', self.disease_id),])