from odoo import api, fields, models


class OSLPatient(models.Model):
    _name = 'osl.hospital.patient'
    _inherit = ['osl.hospital.medic.info']
    _description = 'Patient'

    name = fields.Char()
    description = fields.Text()

    phone = fields.Char(string="Телефон")

    doctor_id = fields.Many2one(
        comodel_name='osl.hospital.doctor',
        string='Doctor',
    )

    insurance_policy_number = fields.Char(size=20)

    history_ids = fields.One2many(
        comodel_name='osl.hospital.doctor.history',
        inverse_name='patient_id',
        string='History Doc/Patient',
        help='History Doc/Patient',
    )

    count_appointments = fields.Integer(
        store=False,
        compute='_compute_count_appointments'
    )

    @api.onchange("phone")
    def _onchange_phone(self):
        if self.phone:
            self.phone = self._phone_format(
                fname="phone", country='',
                force_format="INTERNATIONAL", raise_exception=False,
            ) or self.phone

    def show_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments by Patient',
            'res_model': 'osl.hospital.appointment',
            'view_mode': 'list',
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
        }

    def new_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Appointment by Patient',
            'res_model': 'osl.hospital.appointment',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_patient_id': self.id},
        }

    def _compute_count_appointments(self):
        self.ensure_one()
        for rec in self:
            rec.count_appointments = self.env['osl.hospital.appointment'].search_count([('patient_id', '=', self.id)])
