from odoo import fields, models


class OSLDoctor(models.Model):
    _name = 'osl.hospital.type.disease'
    _description = 'Type disease'

    name = fields.Char()
    description = fields.Text()
