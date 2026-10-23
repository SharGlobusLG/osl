from odoo import api, fields, models


class OSLMedicInfo(models.AbstractModel):
    _name = 'osl.hospital.medic.info'
    _description = 'Medical info'

    blood_type = fields.Selection(
        selection=[
            ('type_1', 'O(I)'),
            ('type_2', 'A(II)'),
            ('type_3', 'B(III)'),
            ('type_4', 'AB(IV)'),
        ],
        string='Blood Type'
    )

    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
    )

    birth_date = fields.Date('Birth Date')

    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        readonly=True,
        store=False,
    )

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if not record.birth_date:
                record.age = 0
                continue

            birth_date = fields.Date.to_date(record.birth_date)
            record.age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )
