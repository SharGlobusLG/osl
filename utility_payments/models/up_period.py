import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class UPApartmentUtility(models.Model):
    """List of month to account charge-payment"""
    _name = 'up.period'
    _description = 'List of periods (months) for which accruals and payments are recorded'

    date = fields.Date(
        string='Date',
        required=True,
    )

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        readonly=True,
        required=True,
    )

    @api.onchange('date')
    def _onchange_date(self):
        """Calculate begin of month"""
        self.ensure_one()
        if self.date:
            self.date = self._month_start(self.date)

    _date_unique = models.Constraint(
        definition='UNIQUE(date)',
        message='Period with same date already exist',
    )

    @api.depends('date')
    def _compute_name(self):
        """Generates a name based on the date"""
        months = [self.env._('January'),
                  self.env._('February'),
                  self.env._('March'),
                  self.env._('April'),
                  self.env._('May'),
                  self.env._('June'),
                  self.env._('July'),
                  self.env._('August'),
                  self.env._('September'),
                  self.env._('October'),
                  self.env._('November'),
                  self.env._('December'),
                  self.env._('December'),
                  ]
        for rec in self:
            if rec.date:
                rec.name = f"{months[rec.date.month - 1]} {rec.date.year}"
            else:
                rec.name = False

    def write(self, vals):
        for rec in self:
            begin_month = self._month_start(rec.date)
            if 'date' in vals and vals['date'] != begin_month:
                vals['date'] = begin_month
        return super().write(vals)

    @api.model
    def action_open_generate_wizard(self):
        """ Action for open wizard
        :return: Action
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'up.period.generate.wizard',
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model
    def _month_start(self, any_date):
        """Перший день місяця для довільної дати."""
        return fields.Date.to_date(any_date).replace(day=1)

    @api.model
    def _get_or_create(self, any_date):
        """Find or Create period for any_day"""
        start = self._month_start(any_date)
        period = self.search([('date', '=', start)], limit=1)
        if not period:
            period = self.create({'date': start})
        return period

    @api.model
    def _ensure_range(self, date_from, date_to):
        """Create all missing periods within the interval [date_from; date_to].
        Returns the records that were created."""
        start = self._month_start(date_from)
        end = self._month_start(date_to)
        if start > end:
            start, end = end, start
        existing = set(self.search([
            ('date', '>=', start),
            ('date', '<=', end),
        ]).mapped('date'))
        new_periods = self.browse()
        current = start
        while current <= end:
            if current not in existing:
                new_periods |= self.create({'date': current})
            current += relativedelta(months=1)
        return new_periods
