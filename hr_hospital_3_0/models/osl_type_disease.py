from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class OSLTypeDisease(models.Model):
    _name = 'osl.hospital.type.disease'
    _description = 'Type disease'
    _parent_store = True
    _parent_name = 'parent_id'
    _rec_name = 'display_name'

    name = fields.Char(
        required=True,
    )

    description = fields.Text()

    parent_id = fields.Many2one(
        comodel_name='osl.hospital.type.disease',
        string='Parent',
        index=True,
        ondelete='restrict',
        domain="[('id', '!=', id)]",
    )

    child_ids = fields.One2many(
        comodel_name='osl.hospital.type.disease',
        inverse_name='parent_id',
        string='Child Diseases',
    )
    parent_path = fields.Char(index=True)

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        if self._has_cycle():
            raise ValidationError(
                "Error: you cannot create a recursive hierarchy. "
                  "A disease cannot be its own parent or ancestor."
            )

    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        if self.parent_id and self.parent_id.id == self.id:
            self.parent_id = False
            return {
                'warning': {
                    'title': 'Invalid parent',
                    'message': 'A disease cannot be its own parent.',
                }
            }
        return {}

    display_name = fields.Char(
        compute='_compute_display_name',
        recursive=True,
        store=True,
        index=True,
    )

    @api.depends('name', 'parent_id.display_name')
    def _compute_display_name(self):
        for record in self:
            if record.parent_id and record.parent_id.display_name:
                record.display_name = f"{record.parent_id.display_name} / {record.name}"
            else:
                record.display_name = record.name or ''

    def unlink(self):
        for record in self:
            if record.child_ids:
                child_names = ', '.join(record.child_ids.mapped('display_name')[:5])
                raise UserError(
                    f"Cannot delete {record.display_name} because it has child diseases: {child_names}\n"
                    "Please delete or re-parent the children first."
                )
        return super().unlink()
