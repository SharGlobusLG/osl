from datetime import date, datetime

from odoo.exceptions import UserError
from odoo.tests import Form, freeze_time, tagged

from .common import OSLTestCommon


@tagged('osl')
class TestHospitalModels(OSLTestCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.doctor = cls.env['osl.hospital.doctor'].create({'name': 'Test Doctor'})
        cls.doctor_2 = cls.env['osl.hospital.doctor'].create({'name': 'Test Doctor #2'})
        cls.patient = cls.env['osl.hospital.patient'].create({'name': 'Test Patient'})

    def test_01_create_appointment(self):
        scheduled_date = datetime(2026, 1, 15, 10, 0)
        appointment = self.env['osl.hospital.appointment'].create({
            'doctor_id': self.doctor.id,
            'patient_id': self.patient.id,
            'scheduled_date': scheduled_date,
        })

        self.assertTrue(appointment)
        self.assertEqual(appointment.state, 'scheduled')
        self.assertEqual(appointment.scheduled_date, scheduled_date)
        self.assertEqual(appointment.doctor_id, self.doctor)
        self.assertEqual(appointment.patient_id, self.patient)

    @freeze_time('2026-01-15 10:00:00')
    def test_02_completed_appointment_onchange_restores_values(self):
        original_date = datetime(2026, 1, 15, 10, 0, 0)
        appointment = self.env['osl.hospital.appointment'].create({
            'state': 'completed',
            'doctor_id': self.doctor.id,
            'patient_id': self.patient.id,
            'scheduled_date': original_date
        })
        form = Form(appointment)
        form.state = 'completed'
        appointment_saved = form.save()
        self.assertFalse(appointment_saved.actual_date)

    def test_disease_parent_recursion_is_rejected(self):
        disease = self.env['osl.hospital.type.disease'].create({'name': 'Disease'})
        with self.assertRaises(UserError):
            disease.write({'parent_id': disease.id})

    def test_history_onchange_clears_exchange_date_before_set_date(self):
        history = self.env['osl.hospital.doctor.history'].create({
            'set_date': date(2026, 1, 15),
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id
        })
        with self.assertRaises(UserError):
            history.write({'exchange_date': date(2026, 1, 10)})
