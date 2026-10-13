from odoo import fields, models


class OSLDoctor(models.Model):
    _name = 'osl.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char()
    description = fields.Text()
