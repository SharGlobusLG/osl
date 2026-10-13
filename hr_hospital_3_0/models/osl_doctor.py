from odoo import fields, models


class OSLDoctor(models.Model):
    _name = 'osl.hospital.doctor'
    _description = 'Doctor'
    _rec_name = 'name'

    name = fields.Char()
    description = fields.Text()

    osl_doctor_category_id = fields.Many2one(
        comodel_name='osl.hospital.doctor.category',
        string='Doctor Category',
        ondelete='restrict',
    )
