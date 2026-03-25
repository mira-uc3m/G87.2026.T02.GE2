"""class for testing the register_project method"""
import unittest
import json
from freezegun import freeze_time
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
main_python_path = os.path.abspath(os.path.join(current_dir, "../../main/python"))

if main_python_path not in sys.path:
    sys.path.insert(0, main_python_path)

from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class TestRegisterProject(unittest.TestCase):
    def setUp(self):
        """Clean up the JSON file before each test."""
        self.manager = EnterpriseManager()
        self.filename = "corporate_operations.json"
        if os.path.exists(self.filename):
            os.remove(self.filename)

    @freeze_time("2024-01-01")
    def test_TC1_valid_case_min_values(self):
        """TC1: Valid case with minimum boundary values."""
        result = self.manager.register_project(
            "B12345678", "PRO01", "10 letters", "HR", "01/01/2025", 50000.00
        )
        self.assertEqual(result, "5a3aa3b610e39ea827afd8d0988c321d")

    @freeze_time("2024-01-01")
    def test_TC2_valid_case_max_description(self):
        """TC2: Valid case with 30-letter description and FINANCE dept."""
        result = self.manager.register_project(
            "B12345678", "PRO02CARTE", "thirty letter description test",
            "FINANCE", "02/02/2026", 50000.01
        )
        self.assertEqual(result, "4750d3c3baf967a10ec433481bc035b0")

    @freeze_time("2024-01-01")
    def test_TC3_valid_case_max_budget(self):
        """TC3: Valid case with max budget and LEGAL dept."""
        result = self.manager.register_project(
            "B12345678", "PRO012", "eleven test", "LEGAL", "30/11/2027", 1000000.00
        )
        self.assertEqual(result, "45fbdd5a7826d17bafb834d6fc208adc")

    @freeze_time("2024-01-01")
    def test_TC4_valid_case_max_acronym(self):
        """TC4: Valid case with max acronym length and LOGISTICS dept."""
        result = self.manager.register_project(
            "B12345678", "PRO012345", "twenty-nine letters test test",
            "LOGISTICS", "31/12/2026", 999999.99
        )
        self.assertEqual(result, "cdeeabd29fa9259f168922a3fa47841e")

    def test_TC5_invalid_cif_not_string(self):
        """TC5: CIF must be a string."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project(123456789, "PRO02", "first test", "LOGISTICS", "02/01/2026", 60000.00)
        self.assertEqual(str(cm.exception), "CIF must be a string")

    def test_TC6_invalid_cif_algorithm(self):
        """TC6: CIF fails validation algorithm pattern."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("AA123456B", "PRO03", "first test", "LOGISTICS", "03/01/2026", 60000.00)
        self.assertEqual(str(cm.exception), "CIF does not pass validation algorithm")

    def test_TC7_project_acronym_not_string(self):
        """TC7: Project acronym must be a string."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345678", True, "second test", "HR", "4/1/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project acronym must be a string")

    def test_TC8_project_acronym_too_short(self):
        """TC8: Project acronym is too short (4)."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("A12345678", 'PR01', "Project for development", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project acronym is too short")

    def test_TC9_project_acronym_too_long(self):
        """TC9: Project acronym is too long (10)."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("A12345678", 'PROJ1234567', "Project for development", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project acronym is too long")

    def test_TC10_project_acronym_invalid_characters(self):
        """TC10: Project acronym contains invalid characters."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("A12345678", 'PROJ_1!', "Project for development", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project acronym cannot contain special characters")

    def test_TC11_project_description_not_string(self):
        """TC11: Project description not a string."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("A12345678", 'PRO03', 12345, "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project description must be a string")

    def test_TC12_project_description_too_short(self):
        """TC12: Project description too short (9)."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("A12345678", 'PRO03', "Inv Desc", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project description is too short")

    def test_TC13_project_description_too_long(self):
        """TC13: Project description too long (31)."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("A12345678", 'PRO03', "project description too long 31", "LEGAL", "21/02/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Project description is too long")

    def test_TC14_department_not_a_string(self):
        """TC14: Department is not a string."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("A12345678", 'PRO03', "description", 123,"21/02/2026", 60000.00)
            self.assertEqual(str(cm.exception), "Department must be a string")

    def test_TC15_department_not_a_valid_entry(self):
        """TC15: Department is not a valid entry."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("A12345678", 'PRO03', "description", 'SALES',"21/02/2026", 60000.00)
            self.assertEqual(str(cm.exception), "Invalid department entry")

    def test_TC16_invalid_date_format(self):
        """TC16: Date must be a string."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("A12345678", 'PRO03', "description", 'SALES', 1022025, 60000.00)
            self.assertEqual(str(cm.exception), "Date must be a string")

    def test_TC17_invalid_date(self):
        """TC17: Invalid date format."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "1022025", 60000.00)
        self.assertEqual(str(cm.exception), "Invalid date format")

    def test_TC18_invalid_day_00_date(self):
        """TC18: Invalid day (00) in date."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "00/05/2025", 60000.00)
        self.assertEqual(str(cm.exception), "Days in date is not a valid value")

    def test_TC19_invalid_day_32_date(self):
        """TC19: Invalid day (32) in date."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "32/05/2026", 60000.00)
        self.assertEqual(str(cm.exception), "Days in date is not a valid value")

    def test_TC20_year_too_low(self):
        """TC20_year_too_low: Year is too low."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "01/01/2024",60000.00)
            self.assertEqual(str(cm.exception), "Date is too early")

    def test_TC21_year_too_high_boundary(self):
        """TC20_year_too_low: Year is too high on the boundary."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "31/12/2028",60000.00)
            self.assertEqual(str(cm.exception), "Date is too late")

    def test_TC22_year_too_high_not_boundary(self):
        """TC20_year_too_low: Year is too high not on the boundary."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "01/01/2029",60000.00)
            self.assertEqual(str(cm.exception), "Date is too late")

    def test_TC23_invalid_day_00_date(self):
        """TC23: Invalid month (00) in date."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "02/00/2025", 60000.00)
        self.assertEqual(str(cm.exception), "Month in date is not a valid value")

    def test_TC24_invalid_day_32_date(self):
        """TC24: Invalid month (13) in date."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "02/13/2025", 60000.00)
        self.assertEqual(str(cm.exception), "Month in date is not a valid value")

    @freeze_time("2026-01-01")
    def test_TC25_date_too_low(self):
        """TC25_date_too_low: Date is too low."""
        past_date = "15/05/2025"
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("A12345678", "PROJ123", "Valid Description", "HR", past_date, 60000.00)

        self.assertEqual(str(cm.exception), "Today's date is after the project's date")

    def test_TC26_budget_not_float(self):
        """TC26: Budget is not a float."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "02/10/2025",'60000')
        self.assertEqual(str(cm.exception), "Budget must be a float")

    def test_TC27_budget_not_valid_format(self):
        """TC27: Budget is not a valid format."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "02/10/2025",60000.001)
        self.assertEqual(str(cm.exception), "Budget must have 2 decimal places")

    def test_TC28_budget_too_low(self):
        """TC28: Budget is too low."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "02/10/2025",
                                                49999.99)
        self.assertEqual(str(cm.exception), "Budget is too low")

    def test_TC29_budget_too_high(self):
        """TC29: Budget is too high."""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project("B12345677", 'PRO00', "Valid description length", "HR", "02/10/2025",
                                                1000000.01)
        self.assertEqual(str(cm.exception), "Budget is too high")

    @freeze_time("2024-01-01")
    def test_TC31_duplicate_entry_error(self):
        """TC31: Requirement CM-FR-01-O3 - Error if same CIF and Acronym already exist."""
        # First registration (Success)
        self.manager.register_project(
            "B12345678", "PRO01", "10 letters", "HR", "01/01/2025", 50000.00
        )
        # Second registration with same CIF and Acronym (Failure)
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.register_project(
                "B12345678", "PRO01", "different description", "HR", "02/01/2025", 55000.00
            )
        self.assertEqual(str(cm.exception), "Project with the same name for the same CIF already existed")

if __name__ == '__main__':
    unittest.main()