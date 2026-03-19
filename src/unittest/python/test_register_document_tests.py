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

if __name__ == '__main__':
    unittest.main()