""" Module that includes the tests of GE2.2 - Function 1 - Room Reservation """
import os.path
from pathlib import Path
import json
from unittest import TestCase
from uc3mtravel import HotelManager
from uc3mtravel import HotelManagementException


class TestRoomReservation(TestCase):
    """ Class to test Function 1: room reservation process """

    __path_tests = str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/data/tests/"
    __path_data = str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/data/"

    @classmethod
    def setUpClass(cls):
        """ Opens input test files with test data and assigns to attributes for the tests to use. Also clear store..."""
        # Load all tests...
        try:
            with open(cls.__path_tests + "f1_tests.json", encoding='UTF-8', mode="r") as f:
                test_data_credit_card = json.load(f)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError:
            test_data_credit_card = []
        cls.__test_data_credit_card = test_data_credit_card
        # Clear the bookings file from possible previous runs...
        all_bookings = cls.__path_data + "/all_bookings.json"
        if os.path.isfile(all_bookings):
            os.remove(all_bookings)
        return True

    def test_room_reservation_tests_ok(self):
        """ TestCases: TC1 -  Expected OK. Checks Card Number is OK. Localizer OK + Booking is stored
                       TC10 - Expected OK. Checks Room Type value DOUBLE. Localizer OK + Booking is stored
                       TC11 - Expected OK. Checks Room Type value SUITE. Localizer OK + Booking is stored """
        for input_data in self.__test_data_credit_card:
            with self.subTest():
                if input_data["idTest"] in ("TC1", "TC10", "TC11"):
                    print("Executing: " + input_data["idTest"])
                    hm = HotelManager()
                    localizer = hm.room_reservation(input_data["creditCardNumber"], input_data["idCard"],
                                                    input_data["nameSurname"], input_data["phoneNumber"],
                                                    input_data["roomType"], input_data["arrival"],
                                                    input_data["numDays"])
                    match input_data["idTest"]:
                        case "TC1":
                            self.assertEqual(localizer, "37b8fbcb885bba0ce1e3727161697d0f")
                        case "TC10":
                            self.assertEqual(localizer, "bb92772ce43c4acac8839a6aae3d7ab6")
                        case "TC11":
                            self.assertEqual(localizer, "abc90c4f85db133e5cfc3e0e482aa886")
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

    def test_room_reservation_tests_ko(self):
        """ TestCases: TC2 - Expected KO. Card Number not comply luhn.
                       TC3 - Expected KO. Card Number is not a number.
                       TC4 - Expected KO. Card Number incorrect length.
                       TC5 - Expected KO. Card Number incorrect length.
                       TC6 - Expected KO. Card Number is not a number.
                       TC7 - Expected KO. Card Number incorrect length.
                       TC8 - Expected KO. Card Number incorrect length.
                       TC9 - Expected KO. Card Number is not a number.
                       TC12 - Expected KO. Card Number incorrect length.
                       TC13 - Expected KO. Card Number incorrect length.
                       TC14 - Expected KO. Card Number is not a number.
                       TC15 - Expected KO. Card Number incorrect length.
                       TC16 - Expected KO. Card Number incorrect length.
                       TC17 - Expected KO. Card Number is not a number.
                       TC18 - Expected KO. Card Number incorrect length.
                       TC19 - Expected KO. Card Number incorrect length.
                       TC20 - Expected KO. Card Number is not a number. """
        for input_data in self.__test_data_credit_card:
            with self.subTest():
                if input_data["idTest"] not in ("TC1", "TC10", "TC11"):
                    print("Executing: " + input_data["idTest"])
                    hm = HotelManager()
                    with self.assertRaises(HotelManagementException) as result:
                        hm.room_reservation(input_data["creditCardNumber"], input_data["idCard"],
                                            input_data["nameSurname"], input_data["phoneNumber"],
                                            input_data["roomType"], input_data["arrival"],
                                            input_data["numDays"])
                    match input_data["idTest"]:
                        case "TC2":
                            self.assertEqual(result.exception.message, "Invalid credit card number provided. Not a valid number.")
                        case "TC3":
                            self.assertEqual(result.exception.message, "Invalid credit card number provided. Invalid characters found.")
                        case "TC4":
                            self.assertEqual(result.exception.message, "Invalid credit card number provided. Invalid length.")
                        case "TC5":
                            self.assertEqual(result.exception.message, "Invalid credit card number provided. Invalid length.")
                        case "TC6":
                            self.assertEqual(result.exception.message, "Invalid name surname provided (length between 10 and 50 characters and separated by space)")
                        case "TC7":
                            self.assertEqual(result.exception.message, "Invalid phone number provided (must be 9 digits)")
                        case "TC8":
                            self.assertEqual(result.exception.message, "Invalid phone number provided (too long)")
                        case "TC9":
                            self.assertEqual(result.exception.message, "Invalid phone number provided (too short)")
                        case "TC12":
                            self.assertEqual(result.exception.message, "Invalid room type provided (must be SINGLE, DOUBLE or SUITE")
                        case "TC13":
                            self.assertEqual(result.exception.message, "Invalid arrival date provided (format must be dd/mm/yyyy")
                        case "TC14":
                            self.assertEqual(result.exception.message, "Invalid arrival date provided (format must be dd/mm/yyyy")
                        case "TC15":
                            self.assertEqual(result.exception.message, "Invalid number of days provided (not a valid number)")
                        case "TC16":
                            self.assertEqual(result.exception.message, "Invalid number of days provided (must be between 1 and 10)")
                        case "TC17":
                            self.assertEqual(result.exception.message, "Invalid number of days provided (must be between 1 and 10)")
                        case "TC18":
                            self.assertEqual(result.exception.message, "Invalid ID Card provided. Must be valid Spanish NIF document")
                        case "TC19":
                            self.assertEqual(result.exception.message, "Invalid ID Card provided. Must be valid Spanish NIF document")
                        case "TC20":
                            self.assertEqual(result.exception.message, "Invalid ID Card provided. Must be valid Spanish NIF document")
