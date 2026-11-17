from odoo import fields, models
from odoo.tools import date_utils


class UPGeneratePeriodWizard(models.TransientModel):
    _name = "up.period.generate.wizard"
    _description = "Auto-filling the list of periods"

    begin_date = fields.Date(
        string='Begin period',
        required=True,
        default=fields.Date.today(),
    )
    end_date = fields.Date(
        string='End period',
        required=True,
        default=date_utils.add(fields.Date.today(), years=1),
    )

    def action_create_period_list(self):
        self.ensure_one()
        created = self.env['up.period']._ensure_range(self.begin_date, self.end_date)
        return {
            'type': 'ir.actions.act_window_close',
            'message': f'{len(created)} new periods created',
        }
