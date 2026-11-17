from odoo import fields, models


class UPApartment(models.Model):
    """List of apartment"""
    _name = 'up.apartment'
    _description = 'List of apartment'

    active= fields.Boolean(default=True)

    name = fields.Char(
        string='Name',
        required=True,
    )

    address = fields.Char(
        string='Address',
        required=True,
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
    )

    apartment_utility_ids = fields.One2many(
        string='Apartment Utility list',
        comodel_name='up.apartment.utility',
        inverse_name='apartment_id',
    )