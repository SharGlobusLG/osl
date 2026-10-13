from odoo import fields, models


class OSLPatient(models.Model):
    _name = 'osl.hospital.patient'
    _description = 'Patient'

    name = fields.Char()
    description = fields.Text()
