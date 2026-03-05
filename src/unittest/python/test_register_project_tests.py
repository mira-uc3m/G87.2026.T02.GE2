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
        """TC8: Project achronym is too short (4)."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("A12345678", 'PR01', "Project for development", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project achronym is too short")

    def test_TC9_project_achronym_too_long(self):
        """TC9: Project achronym is too long (10)."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("A12345678", 'PROJ1234567', "Project for development", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project achronym is too long")

    def test_TC10_project_achronym_invalid_characters(self):
        """TC10: Project achronym contains invalid characters."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("A12345678", 'PROJ_1!', "Project for development", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project achronym cannot contain special characters")

    def test_TC11_project_description_not_string(self):
        """TC11: Project description not a string."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("A12345678", 'PRO03', 12345, "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project description must be a string")

    def test_TC12_project_description_too_short(self):
        """TC12: Project description too short (9)."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("A12345678", 'PRO03', "Inv Desc", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project description is too short")

    def test_TC13_project_description_too_long(self):
        """TC13: Project description too long (31)."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("A12345678", 'PRO03', "project description too long 31", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project description is too long")

    def test_TC14_department_not_a_string(self):
        """TC14: Department is not a string."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("A12345678", 'PRO03', "description", 123,"21/02/2026", 60000.00)
            self.assertEqual(str(cm.exception), "Department must be a string")

    def test_TC15_department_not_a_valid_entry(self):
        """TC15: Department is not a valid entry."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("A12345678", 'PRO03', "description", 'SALES',"21/02/2026", 60000.00)
            self.assertEqual(str(cm.exception), "Invalid department entry")

    def test_TC16_invalid_date_format(self):
        """TC16: Date must be a string."""
        enterprise_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            enterprise_manager.register_project("A12345678", 'PRO03', "description", 'SALES', 1022025, 60000.00)
            self.assertEqual(str(cm.exception), "Date must be a string")

if __name__ == '__main__':
    unittest.main()