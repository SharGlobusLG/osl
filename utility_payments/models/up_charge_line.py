from odoo import fields, models


class UPChargeLine(models.Model):
    """List (lines) charges for apartment"""
    _name = 'up.charge.line'
    _description = 'Utility Charges Line'

    charge_id = fields.Many2one(
        string='Charge',
        comodel_name='up.charge',
        required=True,
        ondelete='cascade',
        readonly=True,
    )

    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product',
        required=True,
        ondelete='restrict',
        domain=[('type_utility_id','!=',False)],
    )

    type_utility_id = fields.Many2one(
        string='Utility',
        related='product_id.type_utility_id',
        store=False,
        readonly=True,
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        readonly=True,
        default=lambda self: self.env.company.currency_id,
    )

    sum = fields.Monetary(
        string='Sum',
        currency_field='currency_id',
    )
