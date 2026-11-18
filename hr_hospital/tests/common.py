from odoo.tests import TransactionCase, new_test_user


class OSLTestCommon(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.patient_user = new_test_user(
            cls.env, login='osl_patient_test', groups='hr_hospital.osl_hospital_group_patient'
        )
        cls.manager_user = new_test_user(
            cls.env, login='osl_manager_test', groups='hr_hospital.osl_hospital_group_manager'
        )
