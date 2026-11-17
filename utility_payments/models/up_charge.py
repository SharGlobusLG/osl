from odoo import api, fields, models
from odoo.orm.commands import Command


class UPCharge(models.Model):
    """List of charges for each apartment and period"""
    _name = 'up.charge'
    _description = 'Utility Charges'

    state = fields.Selection(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('paid', 'Paid'),
        ],
        default='draft',
    )

    apartment_id = fields.Many2one(
        string='Apartment',
        comodel_name='up.apartment',
        required=True,
    )

    period_id = fields.Many2one(
        string='Period',
        comodel_name='up.period',
        required=True,
    )

    date = fields.Date(
        string='Date',
        compute='_compute_total_sum',
        store=True,
    )

    @api.depends('period_id')
    def _compute_date(self):
        """Get date from Period"""
        for record in self:
            record.date = record.period_id.date

    charge_line_ids = fields.One2many(
        comodel_name='up.charge.line',
        inverse_name='charge_id',
        string='Charge lines',
    )

    total_sum = fields.Float(
        string='Total',
        compute='_compute_total_sum',
        store=True,
        # currency_field='currency_id'
    )

    @api.depends('charge_line_ids.sum')
    def _compute_total_sum(self):
        """Calculate total sum of all lines"""
        for record in self:
            record.total_sum = sum(record.charge_line_ids.mapped('sum'))

    def action_reload_lines(self):
        """Reload lines for selected apartment"""
        for record in self:
            if not record.apartment_id and not record.period_id and self.state != 'draft':
                continue

            # Отримуємо дані для табличної частини
            line_vals = record._get_apartment_charge_lines(charge_id=record.id, apartment_id=record.apartment_id.id, period_id=record.period_id.id)

            # Повністю замінюємо табличну частину
            record.charge_line_ids = [
                Command.clear(),
                *[Command.create(vals) for vals in line_vals],
            ]

    @api.model
    def _get_apartment_charge_lines(self, charge_id=None, apartment_id=None, period_id=None):
        """Prepare charge lines for selected apartment."""
        new_lines = []
        if apartment_id and period_id and charge_id:
            apartment_utility_ids = self.env['up.apartment.utility'].search([('apartment_id', "=", apartment_id)])
            for apartment_utility_id in apartment_utility_ids:
                sum = 0
                if apartment_utility_id.calc_type == 'fixed':
                    sum = apartment_utility_id.fixed_sum
                else:
                    sum = 0
                new_lines.append({
                    'charge_id': charge_id,
                    'product_id': apartment_utility_id.product_id.id,
                    'currency_id': apartment_utility_id.currency_id.id,
                    'sum': sum
                })
        return new_lines

    def action_approve(self):
        """Approve charge from form"""
        self.ensure_one()
        self.state = 'approved'

    def action_reject(self):
        """Reject charge from form"""
        self.ensure_one()
        self.state = 'draft'
