import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from helpers.generator import get_UUID, get_token_validation

class TestGenerator(unittest.TestCase):
    def test_get_UUID(self):
        check_data = get_UUID()

        self.assertTrue(len(check_data) == 36, f"Actual Result : {len(check_data)}") # Check if function return specific character length = 36
        self.assertTrue('-' in check_data, f"Actual Result : {check_data}") # Check if function return include symbol '-' in the respond
        self.assertTrue(check_data.isalpha, f"Actual Result : {type(check_data)}") # Check if function return string data type
        
    def test_get_token_validation(self):
        # Positive Case - Valid param
        positive_check_len = 6
        check_data = get_token_validation(positive_check_len)

        self.assertTrue(len(check_data) == positive_check_len, f"Actual Result : {len(check_data)}") # Check if function return specific character length = 6
        self.assertTrue(check_data.isupper(), f"Actual Result : {check_data}") # Check if all char are uppercase
        self.assertTrue(check_data.isalpha, f"Actual Result : {type(check_data)}") # Check if function return string data type

        # Negative Case - Invalid zero as param
        negative_check_len = 0
        check_data = get_token_validation(negative_check_len)
        
        self.assertTrue(len(check_data) != negative_check_len, f"Actual Result : {len(check_data)}") # Check if function return character length is not same with the param
        self.assertEqual(check_data,"Cant't have parameter below 1", f"Actual Result : {check_data}") # Check if its return error message "Cant't have parameter below 1"
        self.assertTrue(check_data.isalpha, f"Actual Result : {type(check_data)}") # Check if function return string data type

        # Negative Case - Invalid negative number as param
        negative_check_len = -4
        check_data = get_token_validation(negative_check_len)
        
        self.assertTrue(len(check_data) != negative_check_len, f"Actual Result : {len(check_data)}") # Check if function return character length is not same with the param
        self.assertEqual(check_data,"Cant't have parameter below 1", f"Actual Result : {check_data}") # Check if its return error message "Cant't have parameter below 1"
        self.assertTrue(check_data.isalpha, f"Actual Result : {type(check_data)}") # Check if function return string data type

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit as e:
        print(f"SystemExit: {e}")
