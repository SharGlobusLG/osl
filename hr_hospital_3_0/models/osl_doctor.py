from odoo import api, fields, models
from odoo.exceptions import ValidationError


class OSLDoctor(models.Model):
    _name = 'osl.hospital.doctor'
    _inherit = 'osl.hospital.medic.info'
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
        compute='_compute_is_intern_mentor',
        store=True,
    )

    mentor = fields.Many2one(
        comodel_name='osl.hospital.doctor',
        string='Mentor',
        ondelete='restrict',
        # compute='_compute_is_intern_mentor',
        domain=lambda self: [('is_intern', '=', False), ('id', '!=', self.id)],
        copy=False,
    )

    @api.depends('doctor_category_id')
    def _compute_is_intern_mentor(self):
        for record in self:
            if record.doctor_category_id:
                record.is_intern = record.doctor_category_id.is_intern
                if not record.doctor_category_id.is_intern:
                    record.mentor = None

    @api.constrains('mentor')
    def _check_mentor(self):
        for record in self:
            if record.mentor.is_intern:
                raise ValidationError("Не можна обрати ментором лікаря, який сам є інтерном")
            if record.mentor.id == record.id:
                raise ValidationError("Не можна обрати ментором себє")
