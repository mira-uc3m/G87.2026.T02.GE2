"""class for testing the register_project method"""
import unittest
import json
import os
from ...main.python.uc3m_consulting.enterprise_manager import EnterpriseManager
from ...main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class TestRegisterProject(unittest.TestCase):
    def setUp(self):
        """Clean up the JSON file before each test."""
        self.filename = "corporate_operations.json"
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_TC5_invalid_cif_not_string(self):
        """TC5: CIF must be a string."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project(123456789, "PRO02", "first test", "LOGISTICS", "02/01/2026", 60000.01)
        self.assertEqual(str(cm.exception), "CIF must be a string")

    def test_TC6_invalid_cif_algorithm(self):
        """TC6: CIF fails validation algorithm pattern."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("AA123456B", "PRO03", "first test", "LOGISTICS", "03/01/2026", 60000.02)
        self.assertEqual(str(cm.exception), "CIF does not pass validation algorithm")

    def test_TC7_project_achronym_not_string(self):
        """TC7: Project achronym must be a string."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("B12345678", True, "second test", "HR", "4/1/2026", 60000.03)
        self.assertEqual(str(cm.exception), "Project achronym must be a string")

    def test_TC8_project_achronym_too_short(self):
        """TC7: Project achronym is too short (4)."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("A12345678", 'PR01', "Project for development", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project achronym is too short")
if __name__ == '__main__':
    unittest.main()