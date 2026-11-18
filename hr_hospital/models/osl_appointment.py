import logging

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import LazyTranslate

from ..constants import APPOINTMENT_STATES, CANCELLED, COMPLETED, SCHEDULED

_logger = logging.getLogger(__name__)

_lt = LazyTranslate(__name__)
APPOINTMENT_DONE = _lt('Appointment already done')

class OSLAppointment(models.Model):
    """Contains a list of patient visits.
    For each visit, its status is important:
    * Scheduled
    * Cancelled
    * Completed
    """
    _name = 'osl.hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection(
        selection=APPOINTMENT_STATES,
        string='Visit State',
        default=SCHEDULED,
        tracking=True
    )

    scheduled_date = fields.Datetime(
        string='Scheduled Date',
        required=True,
        tracking=True
    )

    actual_date = fields.Datetime(
        string='Actual Date'
    )

    doctor_id = fields.Many2one(
        string='Doctor',
        comodel_name='osl.hospital.doctor',
        tracking=True
    )

    patient_id = fields.Many2one(
        string='Patient',
        comodel_name='osl.hospital.patient',
        required=True,
        tracking=True
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
        store=False,
        compute='_compute_count_same_disease'
    )

    def write(self, vals):
        """For scheduled appointments, you cannot change the date or the doctor.
        :param vals: Dictionary with new values for fields. Key = field name
        """
        for rec in self:
            if rec._origin.state == COMPLETED and ('scheduled_date' in vals or 'doctor_id' in vals):
                raise UserError(self.env._(APPOINTMENT_DONE))

        if 'state' in vals and vals['state'] == COMPLETED:
            if self._origin.state == COMPLETED and ('scheduled_date' in vals or 'doctor_id' in vals):
                vals['actual_date'] = fields.Datetime.now()

        return super().write(vals)

    def unlink(self):
        """If a Appointment has already been completed, it cannot be deleted.
        """
        if any(rec._origin.state == COMPLETED for rec in self):
            if self.env.context.get('_force_unlink'):
                return super().unlink()
            raise UserError(
                self.env._("Cannot Delete a Finished Appointment.")
            )
        return super().unlink()

    @api.onchange('actual_date', 'doctor_id')
    def _onchange_scheduled_actual_date_doctor(self):
        """If the Appointment has already been completed, you cannot change the date or the doctor.
        """
        for rec in self:
            if rec._origin.state == COMPLETED:
                rec.actual_date = rec._origin.actual_date
                rec.doctor_id = rec._origin.doctor_id
                return {
                    'warning': {
                        'title': APPOINTMENT_DONE,
                        'message': APPOINTMENT_DONE,
                    }
                }
        return {}

    @api.depends('patient_id', 'doctor_id')
    def _compute_display_name(self):
        """
        :return: The display name consists of several fields
        """
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
        """Opens a form for listing appointments with the same diseases
        :return: 'Action' for open list
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Same Disease List'),
            'res_model': 'osl.hospital.appointment',
            'view_mode': 'list',
            'domain': [("disease_id", "=", self.disease_id.id)],
            'target': 'current',
        }

    @api.depends('disease_id')
    def _compute_count_same_disease(self):
        """
        :return: Number of appointment with the same disease
        """
        self.ensure_one()
        for rec in self:
            rec.count_same_disease = self.env['osl.hospital.appointment'].search_count([('disease_id', '=', self.disease_id.id)])

    @api.model
    def set_appointment_state(self):
        """When setting a new status, if the status is "Completed," the actual date should be filled in automatically.
        """
        now = fields.Datetime.now()
        app_ids = self.search([
            ('scheduled_date', '<=', now),
            ('state', '=', SCHEDULED),
        ])
        for record in app_ids:
            record.state = CANCELLED

    def get_color_state(self):
        """
        :return: Returns the Kanban card color for each state
        """
        self.ensure_one()
        match self.state:
            case 'scheduled':
                return 'lightyellow'
            case 'completed':
                return 'lightgreen'
            case 'cancelled':
                return 'lightpink'
            case _:
                return 'gray'
