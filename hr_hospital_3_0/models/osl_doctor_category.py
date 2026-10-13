from odoo import fields, models


class OSLDoctorCategory(models.Model):
    _name = 'osl.hospital.doctor.category'
    _description = 'Doctor Category'

    name = fields.Char(
        string='Doctor Category',
        required=True,
        copy=False,
        translate=True
    )

    sequence = fields.Integer(string='Sequence')

    is_intern = fields.Boolean(
        string='Is Intern',
        default=False,
        copy=False,
    )

    doctor_ids = fields.One2many(
        comodel_name='osl.hospital.doctor',
        inverse_name='doctor_category_id',
        string='Doctors',
        help='Doctors list',
    )


    _name_unique = models.Constraint(
        definition='UNIQUE(name)',
        message='A doctor category with this name already exists.',
    )

