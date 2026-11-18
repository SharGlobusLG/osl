from odoo import fields, models


class OSLDoctorCategory(models.Model):
    """Contains categories of doctors.
    For each category, you can set flags indicating
    whether it represents an intern or a doctor of the highest category.
    """
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

    is_doc = fields.Boolean(
        string='Is Doc',
        default=False,
        copy=False,
    )

    is_doc_high = fields.Boolean(
        string='Is Doc High category',
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
