import os.path
import unittest
import json
from pathlib import Path
from unittest import TestCase
from uc3mtravel import HotelManager
from uc3mtravel import HotelManagementException


class TestRoomReservation(TestCase):
    """ Class to test Function 1: room reservation process """

    __path_tests = str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/data/tests/"
    __path_data = str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/data/"

    @classmethod
    def setUpClass(self):
        """ Opens input test files with test data and assigns to attributes for the tests to use. Also clear store..."""

        # Load all tests...
        try:
            with open(self.__path_tests + "f1_test_credit_card_number.json", encoding='UTF-8', mode="r") as f:
                data_credit_card = json.load(f)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError:
            data_credit_card = []
        self.__data_credit_card = data_credit_card

        # Clear the bookings file from possible previous runs...
        all_bookings = self.__path_data + "/all_bookings.json"
        if os.path.isfile(all_bookings):
            os.remove(all_bookings)
        return True

    def test_credit_card_number_tc1(self):
        """ TestCase: TC1 - Expected OK. Checks localizer OK + Booking is stored """
        for input_data in self.__data_credit_card:
            if input_data["idTest"] == "TC1":
                hm = HotelManager()
                localizer = hm.room_reservation(input_data["creditCardNumber"], input_data["idCard"],
                                                input_data["nameSurname"], input_data["phoneNumber"],
                                                input_data["roomType"], input_data["arrival"],
                                                input_data["numDays"])
                self.assertEqual(localizer, "d41d8cd98f00b204e9800998ecf8427e")
                try:
                    with open(self.__path_data + "/all_bookings.json", encoding='UTF-8', mode="r") as f:
                        bookings = json.load(f)
                except FileNotFoundError as e:
                    raise HotelManagementException("Wrong file or file path") from e
                except json.JSONDecodeError:
                    bookings = []
                booking_found = False
                for booking in bookings:
                    if booking["idCard"] == input_data["idCard"]:
                        booking_found = True
                self.assertTrue(booking_found)
