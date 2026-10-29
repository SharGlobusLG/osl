
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
        index=True,
        comodel_name='osl.hospital.doctor',
        string='Mentor',
        ondelete='restrict',
        domain=lambda self: [('is_intern', '=', False), ('id', '!=', self.id)],
        copy=False,
    )

    intern_ids = fields.One2many(
        comodel_name='osl.hospital.doctor',
        inverse_name='mentor',
        string='Intern of',
    )

    @api.depends('doctor_category_id')
    def _compute_is_intern_mentor(self):
        '''Ознака того, що кваліфікація є Інтерн, міститься в самій таблиці "osl.hospital.doctor.category"
        Це рішення дозволяє мати кілька категорій, які можуть бути Інтерном.
        Також дає більше свободи користувачеві.
        При цьому зберігаючи надійність перевірки.
        Але треба обережно змінювати існуючі категорії.
        '''
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

    def new_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Appointment by Patient',
            'res_model': 'osl.hospital.appointment',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_doctor_id': self.id},
        }

    def get_appointment_list(self):
        self.ensure_one()
        appointment_list = self.env['osl.hospital.appointment'].search(
            [('doctor_id', '=', self.id)])
        appointment_list = appointment_list.sorted('scheduled_date');
        return appointment_list

    def get_patient_list(self):
        self.ensure_one()
        patient_list = self.env['osl.hospital.patient'].search(
            [('doctor_id', '=', self.id)])
        return patient_list

