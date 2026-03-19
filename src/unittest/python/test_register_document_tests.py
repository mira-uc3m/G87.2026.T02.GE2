"""class for testing the register_project method"""
import unittest
import json
import os
from ...main.python.uc3m_consulting.enterprise_manager import EnterpriseManager
from ...main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class TestRegisterProject(unittest.TestCase):
    def setUp(self):
        self.manager = EnterpriseManager()
        self.input_folder = "./input/"
        self.storage_file = "all_documents.json"

        # Create input directory if it doesn't exist
        if not os.path.exists(self.input_folder):
            os.makedirs(self.input_folder)

        # Clear storage file before each test
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)

    def tearDown(self):
        """Clean up created files after tests."""
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)

    def create_test_file(self, filename, content):
        """Helper to create files with a given (potentially broken) string."""
        path = os.path.join(self.input_folder, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_TC01_valid_pdf(self):
        """TC01: Valid JSON with .pdf extension."""
        content = '{"PROJECT_ID":"d2a7ca3223cd13b9a61f0e092aaaa140", "FILENAME":"AB12CD34.pdf"}'
        path = self.create_test_file("valid1.json", content)

        result = self.manager.register_document(path)
        self.assertEqual(len(result), 64) # Check if it's a SHA-256 string

    def test_TC02_valid_docx(self):
        """TC02: Valid JSON with .docx extension."""
        content = '{"PROJECT_ID":"d2a7ca3223cd13b9a61f0e092aaaa140", "FILENAME":"AB12CD34.docx"}'
        path = self.create_test_file("valid2.json", content)

        result = self.manager.register_document(path)
        self.assertEqual(len(result), 64)

    def test_TC03_valid_docx(self):
        """TC02: Valid JSON with .xlsx extension."""
        content = '{"PROJECT_ID":"d2a7ca3223cd13b9a61f0e092aaaa140", "FILENAME":"AB12CD34.xlsx"}'
        path = self.create_test_file("valid3.json", content)

        result = self.manager.register_document(path)
        self.assertEqual(len(result), 64)

if __name__ == '__main__':
    unittest.main()