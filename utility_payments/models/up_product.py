from odoo import fields, models


class UPProductProduct(models.Model):
    """Update product product model"""
    _name = 'product.product'
    _inherit = ['product.product']

    type_utility_id = fields.Many2one(
        comodel_name='up.type.utility',
        string='Type of Utility',
        ondelete='restrict',
    )
    personal_account = fields.Char(
        string='Personal Account',
        )

    provider_id = fields.Many2one(
        string='Provider',
        comodel_name='res.partner',
    )
