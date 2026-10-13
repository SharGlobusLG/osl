from odoo import fields, models


class OSLPatient(models.Model):
    _name = 'osl.hospital.patient'
    _inherit = 'osl.hospital.medic.info'
    _description = 'Patient'

    name = fields.Char()

    description = fields.Text()

    insurance_policy_number = fields.Char(size=20)