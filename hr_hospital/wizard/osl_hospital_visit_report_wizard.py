from datetime import datetime, time, timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError

from ..constants import COMPLETED


class OSLVisitReportWizard(models.TransientModel):
    _name = 'visit.report.wizard'
    _description = "Візард формування звіту по візитах пацієнтів"

    doctor_ids = fields.Many2many(
        comodel_name='osl.hospital.doctor',
        string='Лікарі',
    )
    patient_ids = fields.Many2many(
        comodel_name='osl.hospital.patient',
        string='Пацієнти',
    )
    date_start = fields.Date(string='Початок періоду')
    date_end = fields.Date(string='Кінець періоду')
    only_completed = fields.Boolean(string='Лише завершені візити')
    disease_ids = fields.Many2many(
        comodel_name='osl.hospital.type.disease',
        string='Хвороба',
    )

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        context = self.env.context
        active_ids = context.get('active_ids') or ([context['active_id']] if context.get('active_id') else [])
        active_model = context.get('active_model')

        if active_ids and active_model == 'osl.hospital.patient' and 'patient_ids' in fields_list:
            values['patient_ids'] = [fields.Command.set(active_ids)]
        elif active_ids and active_model == 'osl.hospital.doctor' and 'doctor_ids' in fields_list:
            values['doctor_ids'] = [fields.Command.set(active_ids)]

        return values

    def action_view_report(self):
        self.ensure_one()
        if self.date_start and self.date_end and self.date_start > self.date_end:
            raise ValidationError('Початок періоду не може бути пізніше за його кінець.')

        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))
        if self.date_start:
            domain.append(('scheduled_date', '>=', datetime.combine(self.date_start, time.min)))
        if self.date_end:
            domain.append(('scheduled_date', '<', datetime.combine(self.date_end + timedelta(days=1), time.min)))
        if self.only_completed:
            domain.append(('state', '=', COMPLETED))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Звіт по візитах',
            'res_model': 'osl.hospital.appointment',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
            'context': {'group_by':'disease_id'},
        }
