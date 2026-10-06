from odoo.tests.common import TransactionCase


class TestTmsDriver(TransactionCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()

        self.stage = self.env["tms.stage"].create(
            {
                "name": "Test Stage",
                "stage_type": "driver",
                "sequence": 1,
            }
        )

        self.driver = self.env["tms.driver"].create(
            {
                "name": "Test Driver",
                "is_external": True,
                "driver_type": "terrestrial",
                "driver_license_number": "ABC123456",
                "driver_license_type": "B",
                "distance_traveled": 1000,
                "distance_traveled_uom": "km",
                "driving_experience_years": 5,
            }
        )

    def test_driver_creation(self):
        self.driver._default_stage_id()

        self.assertTrue(self.driver, "Driver wasn't created successfully")
        self.assertEqual(
            self.driver.name, "Test Driver", "Driver name should be 'Test Driver'"
        )
        self.assertTrue(self.driver.is_external, "Driver should be marked as external")
        self.assertEqual(
            self.driver.driver_type,
            "terrestrial",
            "Driver type should be 'terrestrial'",
        )
        self.assertEqual(
            self.driver.driver_license_number,
            "ABC123456",
            "Driver license number should be 'ABC123456'",
        )
        self.assertEqual(
            self.driver.driver_license_type, "B", "Driver license type should be 'B'"
        )
        self.assertEqual(
            self.driver.distance_traveled, 1000, "Distance traveled should be 1000"
        )
        self.assertEqual(
            self.driver.driving_experience_years,
            5,
            "Driving experience years should be 5",
        )
        self.assertTrue(
            self.driver.stage_id, "Driver stage should be correctly assigned"
        )

    def test_vehicle_relation_inverse(self):
        field = self.env["tms.driver"]._fields["vehicles_ids"]

        self.assertEqual(field.model_name, "tms.driver")
        self.assertEqual(field.comodel_name, "fleet.vehicle")
        self.assertEqual(field.inverse_name, "tms_driver_id")

        inverse = self.env["fleet.vehicle"]._fields[field.inverse_name]

        self.assertEqual(inverse.model_name, "fleet.vehicle")
        self.assertEqual(inverse.comodel_name, "tms.driver")

    def test_res_partner_unlink_regression(self):
        partner = self.env["res.partner"].create(
            {
                "name": "TMS partner unlink regression test",
            }
        )

        partner.unlink()

        self.assertFalse(partner.exists())
