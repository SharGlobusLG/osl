from odoo import fields, models, api
from odoo.orm.commands import Command


class UPPayment(models.Model):
    """List of payments for each apartment"""
    _name = 'up.payment'
    _description = 'Utility Payment'

    state = fields.Selection(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('approved', 'Approved'),
        ],
        default='draft',
    )

    apartment_id = fields.Many2one(
        string='Apartment',
        comodel_name='up.apartment',
        required=True,
    )

    payment_line_ids = fields.One2many(
        comodel_name='up.payment.line',
        inverse_name='payment_id',
        string='Payment lines',
    )

    total_sum = fields.Float(
        string='Total',
        compute='_compute_total_sum',
        store=True,
        #currency_field='currency_id'
    )

    @api.depends('payment_line_ids.sum')
    def _compute_total_sum(self):
        """Calculate total sum of all lines"""
        for record in self:
            record.total_sum = sum(record.payment_line_ids.mapped('sum'))

    def action_reload_lines(self):
        """Reload lines for selected apartment"""
        for record in self:
            if not record.apartment_id and not record.period_id and self.state != 'draft':
                continue

            # obtain data for lines
            line_vals = record._get_apartment_charge_lines(payment_id=record.id, apartment_id=record.apartment_id.id)

            # exchange lines with new ones
            record.payment_line_ids = [
                Command.clear(),
                *[Command.create(vals) for vals in line_vals],
            ]

    @api.model
    def _get_apartment_charge_lines(self, payment_id=None, apartment_id=None):
        """Prepare payment lines for selected apartment."""
        new_lines = []
        if apartment_id and payment_id:
            query = """
                WITH cp AS
                  (SELECT up_charge.period_id AS period_id,
                          product_id AS product_id,
                          SUM AS SUM
                   FROM up_charge_line cl
                   LEFT JOIN up_charge ON (up_charge.id = cl.charge_id)
                   WHERE up_charge.apartment_id = %(apartment_id)s
                    AND up_charge.state = 'approved'
                   UNION SELECT pl.period_id AS period_id,
                                pl.product_id AS product_id, - SUM AS SUM
                   FROM up_payment_line AS pl
                   LEFT JOIN up_payment ON (up_payment.id = pl.payment_id)
                   WHERE up_payment.apartment_id = %(apartment_id)s
                        AND pl.payment_id <> %(payment_id)s
                        AND up_payment.state = 'approved'
                   )
                SELECT %(payment_id)s AS payment_id,
                       period_id AS period_id,
                       product_id AS product_id,
                       sum(SUM) AS SUM
                FROM cp
                GROUP BY payment_id,
                         period_id,
                         product_id            
            """
            params = {
                'apartment_id': apartment_id,
                'payment_id': payment_id,
            }
            self.env.cr.execute(query, params)
            new_lines = self.env.cr.dictfetchall()
        return new_lines

    def action_approve(self):
        """Approve payment from form"""
        self.ensure_one()
        self.state = 'approved'

    def action_reject(self):
        """Reject payment from form"""
        self.ensure_one()
        self.state = 'draft'
