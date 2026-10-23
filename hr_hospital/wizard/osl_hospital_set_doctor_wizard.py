import logging

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class OSLSetDoctorWizard(models.TransientModel):
    _name = "mass.reassign.doctor.wizard"
    _description = "Візард масового перевизначення персонального лікаря для пацієнтів"

    patient_ids = fields.Many2many(
        comodel_name="osl.hospital.patient",
        string='Patients',
        readonly=True,
    )

    doctor_id = fields.Many2one(
        comodel_name="osl.hospital.doctor",
        string='Doctor',
        required=True,
    )

    exchange_date = fields.Date(
        string='Doctor Exchange Date',
        required=True,
        default=fields.Date.today(),
    )

    def action_confirm(self):
        self.ensure_one()
        if not self.doctor_id:
            raise UserError("Please select doctor")
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        context = self.env.context

        if (
            'patient_ids' in fields_list
            and context.get('active_model') == 'osl.hospital.patient'
        ):
            patient_ids = context.get('active_ids', [])
            if patient_ids:
                values['patient_ids'] = [fields.Command.set(patient_ids)]

        return values

    def action_set_doctor(self):
        for patient in self.patient_ids:
            history = self.env['osl.hospital.doctor.history'].search([
                ('patient_id', '=', patient.id),
                ('active', '=', True),
            ])

            history.write({
                'active': False,
                'exchange_date': self.exchange_date,
            })

            patient.doctor_id = self.doctor_id
            self.env['osl.hospital.doctor.history'].create({
                'patient_id': patient.id,
                'doctor_id': self.doctor_id.id,
                'set_date': self.exchange_date,
            })

        return {'type': 'ir.actions.act_window_close'}
