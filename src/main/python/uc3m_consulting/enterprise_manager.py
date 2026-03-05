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
