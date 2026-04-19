# import pytest
from weather_main import City, UserInputs
from unittest.mock import patch


class TestCity:

    def setup_method(self, method):
        # print(f"Setting up {method}")
        # self.city1 = City("kota", "india") #----Alternate
        self.cities = [
            City("kota", "india"),
            City("Kota", "India"),# Case insensitive
            City("New delhi", "India"),
            City("Jaipur", "India")# Returns first one
        ]
    
    def teardown_method(self, method):
        # print(f"Tearing down {method}")
        # del self.city1 #----Alternate
        self.cities.clear()

    def test_get_coords_csv(self):
        assert self.cities[0].get_coords_csv() == (25.18,75.83)
        assert self.cities[1].get_coords_csv() == (25.18,75.83)
        assert self.cities[2].get_coords_csv() == (28.6139,77.2089)
        assert self.cities[3].get_coords_csv() == (26.9,75.8)

class TestUserInputs:
    @patch("builtins.input")# for input
    @patch("weather_main.City")

    def test_get_user_city_coords(self, mock_city, mock_input):
        """
        Tests the valid case first time
        """
        #1. Simulate to enter "Kota" and then "India"
        mock_input.side_effect = ["kota", "india"] # inputs to be used
        mock_city.return_value.coords = (25.18,75.83) # mock output

        #2. Execute
        ui = UserInputs.__new__(UserInputs)
        coords = ui.get_user_city_coords()

        #3. Assert
        assert coords == (25.18,75.83)
        assert mock_input.call_count == 2# confirming that user inputs were asked 2 times

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("weather_main.City")
    def test_get_user_city_coords_invalid(self, mock_city, mock_print, mock_input):
        """
        Tests the invalid case first time and then valid case
        """
        #1. inputs for test
        mock_input.side_effect = ["1111","nonExistingCity","Kota","3232", "nonExistingCntry","india"] # inputs to be used

        #2. Ask class to return True False sequence
        # "nonExistingCity" : False, "Kota" : True
        mock_city.city_name_present.side_effect = [False, True]
        mock_city.city_country_matches.side_effect = [False, True]

        #3. Mock coordinates for mock city
        mock_city.return_value.coords = (25.18,75.83) # mock output

        #4. Execute
        ui = UserInputs.__new__(UserInputs)
        coords = ui.get_user_city_coords()

        #3. Assert
        #print all the messages printed
        #Note: It may fail the "assert_called_with" i.e. the last calls of mock_print
        # print(f"\nACTUAL PRINT CALLS: {mock_print.call_args_list}")

        #assert error messages printed
        mock_print.assert_any_call("Enter only characters")
        mock_print.assert_any_call("City 'nonExistingCity' not found in database.")
        mock_print.assert_any_call("Enter only characters")
        #Last print message
        mock_print.assert_called_with("City 'Kota' not found in 'nonExistingCntry' in database.")

        #assert any input call
        mock_input.assert_any_call("Enter a city name: ")
        #assert last input call
        mock_input.assert_called_with("Enter country name: ")
        assert coords == (25.18,75.83)
        assert mock_input.call_count == 6# confirming that user inputs were asked 6 times
        assert mock_print.call_count == 4# assert that total messages printed 4 times
