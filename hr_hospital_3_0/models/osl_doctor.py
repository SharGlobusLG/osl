from odoo import fields, models, api


class OSLDoctor(models.Model):
    _name = 'osl.hospital.doctor'
    _description = 'Doctor'
    _rec_name = 'name'

    name = fields.Char()
    description = fields.Text()

    doctor_category_id = fields.Many2one(
        comodel_name='osl.hospital.doctor.category',
        string='Doctor Category',
        ondelete='restrict',
    )

    user = fields.Many2one(
        comodel_name='res.users',
        string='User',
    )

    is_intern = fields.Boolean(
        string='Intern',
        compute='_compute_is_intern',
        store=True,
    )

    mentor = fields.Many2one(
        comodel_name='osl.hospital.doctor',
        string='Mentor',
        ondelete='restrict',
        copy=False,
    )


    @api.depends('doctor_category_id')
    def _compute_is_intern(self):
        for record in self:
            if record.doctor_category_id:
                record.is_intern =  record.doctor_category_id.is_intern



