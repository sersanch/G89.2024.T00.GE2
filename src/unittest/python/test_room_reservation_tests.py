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
                test_data_f1 = json.load(f)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError:
            test_data_f1 = []
        cls.__test_data_f1 = test_data_f1
        # Clear the bookings file from possible previous runs...
        all_bookings = cls.__path_data + "/all_bookings.json"
        if os.path.isfile(all_bookings):
            os.remove(all_bookings)
        return True

    @classmethod
    def tearDownClass(cls):
        """ Deletes tmp file created during tests... """
        tmp = cls.__path_data + "/tests/tmp_test_data.json"
        if os.path.isfile(tmp):
            os.remove(tmp)
        return True

    def test_room_reservation_tests_ok(self):
        """ TestCases: TC1 -  Expected OK. Checks Card Number is OK. Localizer OK + Booking is stored
                       TC10 - Expected OK. Checks Room Type value DOUBLE. Localizer OK + Booking is stored
                       TC11 - Expected OK. Checks Room Type value SUITE. Localizer OK + Booking is stored """
        for input_data in self.__test_data_f1:
            if input_data["idTest"] in ("TC1", "TC10", "TC11"):
                with self.subTest(input_data["idTest"]):
                    print("Executing: " + input_data["idTest"])
                    hm = HotelManager()
                    localizer = hm.room_reservation(input_data["creditCardNumber"], input_data["idCard"],
                                                    input_data["nameSurname"], input_data["phoneNumber"],
                                                    input_data["roomType"], input_data["arrival"],
                                                    input_data["numDays"])
                    match input_data["idTest"]:
                        case "TC1":
                            self.assertEqual(localizer, "3ff517743faae67b33ddefa77163099d")
                        case "TC10":
                            self.assertEqual(localizer, "a5873426af2a796779344f7ce25009c8")
                        case "TC11":
                            self.assertEqual(localizer, "3456311fa06a9a4d139681398525b869")
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
        """ TestCases: TC2 to TC20 - Expected KO. Different errors. """
        for input_data in self.__test_data_f1:
            if input_data["idTest"] not in ("TC1", "TC10", "TC11"):
                with self.subTest(input_data["idTest"]):
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
