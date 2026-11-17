from datetime import date, datetime

from psycopg2.errors import UniqueViolation

from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form, freeze_time, tagged, TransactionCase


@tagged('osl')
class TestHospitalModels(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_01_create_period(self):
        period = datetime(2026, 1, 15, 10, 0)
        self.env['up.period'].create({'date': period})
        with self.assertRaises(UniqueViolation):
            self.env['up.period'].create({'date': period})