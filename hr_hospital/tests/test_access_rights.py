from odoo.tests import tagged

from .common import OSLTestCommon


@tagged('osl')
class TestAppointmentAccessRights(OSLTestCommon):

    def test_patient_can_only_read_appointments(self):
        appointment = self.env['osl.hospital.appointment']
        patient_model = appointment.with_user(self.patient_user)

        self.assertTrue(patient_model.has_access('read'))
        self.assertFalse(patient_model.has_access('create'))
        self.assertFalse(patient_model.has_access('write'))
        self.assertFalse(patient_model.has_access('unlink'))

    def test_manager_can_read_and_write_appointments(self):
        appointment = self.env['osl.hospital.appointment']
        manager_model = appointment.with_user(self.manager_user)

        self.assertTrue(manager_model.has_access('read'))
        self.assertTrue(manager_model.has_access('write'))
        self.assertFalse(manager_model.has_access('create'))
        self.assertFalse(manager_model.has_access('unlink'))
