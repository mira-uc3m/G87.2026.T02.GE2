"""Module """
import hashlib
import json
import os
import re

from . import ProjectDocument
from .enterprise_management_exception import EnterpriseManagementException

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self, company_cif: str, project_acronym: str, project_description: str, department: str, date: str, budget: float):
        """Method for registering the project"""
        # CIF Validation
        if not isinstance(company_cif, str):
            raise EnterpriseManagementException("CIF must be a string")
        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("CIF does not pass validation algorithm")

        # Project acronym Validation
        if not isinstance(project_acronym, str):
            raise EnterpriseManagementException("Project acronym must be a string")
        if len(project_acronym) < 5:
            raise EnterpriseManagementException("Project acronym is too short")
        if len(project_acronym) > 10:
            raise EnterpriseManagementException("Project acronym is too long")
        if not project_acronym.isalnum():
            raise EnterpriseManagementException("Project acronym cannot contain special characters")

        # Project Description Validation
        if not isinstance(project_description, str):
            raise EnterpriseManagementException("Project description must be a string")
        if len(project_description) < 10:
            raise EnterpriseManagementException("Project description is too short")
        if len(project_description) > 30:
            raise EnterpriseManagementException("Project description is too long")

        # Department Validation
        if not isinstance(department, str):
            raise EnterpriseManagementException("Department must be a string")
        if department not in ['LEGAL', 'HR', 'FINANCE', 'LOGISTICS']:
            raise EnterpriseManagementException("Invalid department")

        # Date Validation
        if not isinstance(date, str):
            raise EnterpriseManagementException("Date must be a string")
        if not isinstance(budget, float):
            raise EnterpriseManagementException("Budget must be a float")
        if not abs(budget - round(budget, 2)) < 1e-9:
            raise EnterpriseManagementException("Budget must have 2 decimal places")
        if budget < 50000:
            raise EnterpriseManagementException("Budget is too low")
        if budget > 1000000:
            raise EnterpriseManagementException("Budget is too high")

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

        # Start of Function Logic
        # Load data from file and check for existing project with same CIF and Project acronym (CM-FR-01-O3)
        file_path = "corporate_operations.json"
        data = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

        for entry in data:
            if entry["company_cif"] == company_cif and entry["acronym"] == project_acronym:
                raise EnterpriseManagementException("Project with the same name for the same CIF already existed")

        # Generate Project ID (CM-FR-01-P2)
        hash_input = f"{company_cif}{project_acronym}"
        project_id = hashlib.md5(hash_input.encode()).hexdigest()

        # Create JSON object to insert into file (CM-FR-01-O1, O2)
        new_project = {
            "project_id": project_id,
            "company_cif": company_cif,
            "acronym": project_acronym,
            "description": project_description,
            "department": department,
            "date": date,
            "budget": budget
        }
        data.append(new_project)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return project_id

    def register_document(self, input_file: str):
        # Load the file
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        project_id = data["PROJECT_ID"]
        filename = data["FILENAME"]

        # Create the document object and get the signature
        my_doc = ProjectDocument(project_id, filename)
        signature = my_doc.document_signature

        # Save to all_documents.json
        storage_file = "all_documents.json"
        all_docs = []
        if os.path.exists(storage_file):
            with open(storage_file, "r") as f:
                all_docs = json.load(f)

        all_docs.append(my_doc.to_json())

        with open(storage_file, "w") as f:
            json.dump(all_docs, f, indent=4)

        return signature

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