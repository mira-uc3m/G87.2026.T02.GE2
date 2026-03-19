"""Module """
import re
from .enterprise_management_exception import EnterpriseManagementException

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self, company_cif: str, project_achronym: str, project_description: str, department: str, date: str, budget: float):
        """Method for registering the project"""
        # TC5: Validate Type
        if not isinstance(company_cif, str):
            raise EnterpriseManagementException("CIF must be a string")
        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("CIF does not pass validation algorithm")
        if not isinstance(project_achronym, str):
            raise EnterpriseManagementException("Project achronym must be a string")
        if len(project_achronym) < 5:
            raise EnterpriseManagementException("Project achronym is too short")
        if len(project_achronym) > 10:
            raise EnterpriseManagementException("Project achronym is too long")
        if not project_achronym.isalnum():
            raise EnterpriseManagementException("Project achronym cannot contain special characters")
        if not isinstance(project_description, str):
            raise EnterpriseManagementException("Project description must be a string")
        if len(project_description) < 10:
            raise EnterpriseManagementException("Project description is too short")
        if len(project_description) > 30:
            raise EnterpriseManagementException("Project description is too long")
        if not isinstance(department, str):
            raise EnterpriseManagementException("Department must be a string")
        if department not in ['LEGAL', 'HR', 'FINANCE', 'LOGISTICS']:
            raise EnterpriseManagementException("Invalid department")
        if not isinstance(date, str):
            raise EnterpriseManagementException("Date must be a string")
        if not isinstance(budget, float):
            raise EnterpriseManagementException("Budget must be a float")
        if not (abs(budget * 10 - round(budget * 10)) < 0.0001 and abs(budget * 100 - round(budget * 100)) < 0.0001):
            raise EnterpriseManagementException("Budget must have 2 decimal places")

        # Extract numerical components to perform individual if-statement checks
        try:
            date_parts = date.split("/")
            if len(date_parts) != 3:
                raise EnterpriseManagementException("Invalid date format")

            day = int(date_parts[0])
            month = int(date_parts[1])
            year = int(date_parts[2])
        except (ValueError, IndexError):
            raise EnterpriseManagementException("Invalid date format")

        if day < 1 or day > 31:
            raise EnterpriseManagementException("Days in date is not a valid value")
        if month < 1 or month > 12:
            raise EnterpriseManagementException("Month in date is not a valid value")
        if year < 2025:
            raise EnterpriseManagementException("Date is too early")
        if year > 2027:
            raise EnterpriseManagementException("Date is too late")
        pass

    @staticmethod
    def validate_cif(cif: str) -> bool:
        """
        Returns True if the CIF received is a valid Spanish CIF pattern,
        otherwise returns False.
        """
        # CIF Pattern: 1 Letter + 7 Digits + 1 Control Character (Letter or Digit)
        cif_pattern = r'^[A-Z][0-9]{7}[A-Z0-9]$'

        if not cif or not re.match(cif_pattern, cif):
            return False

        return True
