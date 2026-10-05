from odoo import fields, models


class OSLDoctor(models.Model):
    _name = 'osl.hospital.appointment'
    _description = 'Appointment'

    name = fields.Char()
    description = fields.Text()
