import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from helpers.converter import calculate_distance

class TestConverter(unittest.TestCase):
    def test_calculate_distance(self):
        # Positive Case - Difference coordinate
        coor1 = '-6.226838579766097,106.82157923228753'
        coor2 = '-6.259654828396329,106.81549274337338'
        check_data = calculate_distance(coord1=coor1, coord2=coor2)

        self.assertTrue(check_data.is_integer, f"Actual Result : {type(check_data)}") # Check if the function returned decimal (number) data type
        self.assertGreater(check_data, 0, f"Actual Result : {check_data}") # Check if the function returned distance more 0 meter

        self.assertTrue(0.1 < check_data < 4000, f"Actual Result : {check_data}") # Check if the function returned distance more than 0.1 meter and less than 4000 meter. in maps its about 3000 meter

        # Negative Case - Same coordinate
        coor1 = '-6.226838579766097,106.82157923228753'
        coor2 = '-6.226838579766097,106.82157923228753'
        check_data = calculate_distance(coord1=coor1, coord2=coor2)

        self.assertTrue(check_data.is_integer) # Check if the function returned decimal (number) data type
        self.assertEqual(check_data, 0, f"Actual Result : {check_data}") # Check if the function returned distance equal to 0 meter

        # Negative Case - Empty coordinate
        coor1 = '-6.226838579766097,106.82157923228753'
        coor2 = None
        check_data = calculate_distance(coord1=coor1, coord2=coor2)

        self.assertTrue(check_data.isalpha) # Check if the function returned string data type
        self.assertEqual(check_data, "Invalid coordinate. Cannot be empty" , f"Actual Result : {check_data}") # Check if the function returned distance equal to "Invalid coordinate. Cannot be empty"
        
if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit as e:
        print(f"SystemExit: {e}")
