from odoo import fields, models


class OSLTypeDisease(models.Model):
    _name = 'osl.hospital.type.disease'
    _description = 'Type disease'

    name = fields.Char()
    description = fields.Text()
