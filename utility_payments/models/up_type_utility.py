from odoo import fields, models


class UPTypeUtility(models.Model):
    """Types of utility model"""
    _name = 'up.type.utility'
    _description = 'Apartment'
    _order = 'sequence'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )

    active = fields.Boolean(default=True)

    sequence = fields.Integer(default=100)

    _name_unique = models.Constraint(
        definition='UNIQUE(name)',
        message='A Type of Utility with same name already exists.',
    )
