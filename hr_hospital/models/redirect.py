import logging

from odoo import models

_logger = logging.getLogger(__name__)

MODULE = "hr_hospital"

class IrModuleModule(models.Model):
    _inherit = "ir.module.module"
    def _button_immediate_function(self, function):
        res = super()._button_immediate_function(function)
        if MODULE in self.mapped("name"):
            menu = self.env.ref(f"{MODULE}.osl_hospital_menu_patient", raise_if_not_found=False)
            if menu:
                res = {
                    "type": "ir.actions.client",
                    "tag": "reload",
                    "params": {"menu_id": menu.id},
                }
        return res