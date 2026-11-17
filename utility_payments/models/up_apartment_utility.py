from odoo import fields, models


class UPApartmentUtility(models.Model):
    """List (lines) of Utility of each Apartment"""
    _name = 'up.apartment.utility'
    _description = 'List of Utility of each Apartment'

    apartment_id = fields.Many2one(
        string='Apartment',
        comodel_name='up.apartment',
        required=True,
        ondelete='restrict',
    )

    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product',
        required=True,
        ondelete='restrict',
        domain=[('type_utility_id', '!=', False)],
    )

    type_utility_id = fields.Many2one(
        string='Utility',
        related='product_id.type_utility_id',
        store=False,
        readonly=True,
    )

    calc_type = fields.Selection(
        selection=[('fixed', 'Fixed sum'), ('prev', 'Previous month'), ('none', 'None')],
        string='Calculation Type',
        default='fixed',
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        readonly=True,
        default=lambda self: self.env.company.currency_id,
    )

    fixed_sum = fields.Monetary(
        string='Fixed sum',
        currency_field='currency_id',
    )
