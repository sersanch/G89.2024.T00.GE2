""" Module that includes the tests of GE2.2 - Function 3 - Guest Checkout """
import hashlib
import unittest
import os.path
import json
from pathlib import Path
from datetime import datetime
from freezegun import freeze_time
from uc3mtravel import HotelManager
from uc3mtravel import HotelManagementException


class TestGuestCheckout(unittest.TestCase):
    """ Class to test Function 3: guest checkout process """

    __path_tests = str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/data/tests/"
    __path_data = str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/data/"

    @classmethod
    def setUpClass(cls):
        """ Opens input test file with test data and assigns to attributes for the tests to use. Also clear checkouts store..."""
        # Load all tests...
        try:
            with open(cls.__path_tests + "f3_tests.json", encoding='UTF-8', mode="r") as f:
                test_data_f3 = json.load(f)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path searching for tests data file") from e
        except json.JSONDecodeError:
            test_data_f3 = []
        cls.__test_data_f3 = test_data_f3
        # Clear the checkouts file from possible previous runs...
        all_checkouts = cls.__path_data + "/all_checkouts.json"
        if os.path.isfile(all_checkouts):
            os.remove(all_checkouts)
        return True

    @freeze_time("2024-06-16")
    def test_guest_checkout_tests_all_ok(self):
        """ TestCases: TC5, TC6, TC8 - Expected OK. Checks call result is True, and checkout is added to checkouts store """
        for index, input_data in enumerate(self.__test_data_f3):
            if index + 1 in [5, 6, 8]:  # TC5, TC6, TC8 are ok tests...
                test_id = "TC" + str(index + 1)
                with self.subTest(test_id):
                    print("Executing: " + test_id)
                    hm = HotelManager()
                    ok_checkout = hm.guest_checkout(input_data["roomKey"])
                    self.assertTrue(ok_checkout)
                    try:
                        with open(self.__path_data + "all_checkouts.json", encoding='UTF-8', mode="r") as f:
                            checkouts = json.load(f)
                    except FileNotFoundError as e:
                        raise HotelManagementException("Wrong file or file path") from e
                    except json.JSONDecodeError:
                        checkouts = []
                    checkout_found = False
                    for checkout in checkouts:
                        if checkout["roomKey"] == input_data["roomKey"]:
                            checkout_found = True
                    self.assertTrue(checkout_found)

    @freeze_time("2024-06-16")
    def test_guest_checkout_tests_ko(self):
        """ TestCases KO: TC1, TC2, TC3, TC4, TC7... """
        for index, input_data in enumerate(self.__test_data_f3):
            if index + 1 not in [5, 6, 8]:  # The ones ok...
                test_id = "TC" + str(index + 1)
                with self.subTest(test_id):
                    print("Executing: " + test_id)
                    hm = HotelManager()
                    with self.assertRaises(HotelManagementException) as result:
                        if test_id in ["TC2"]:  # This test case needs to simulate that stays file does not exist...
                            stays_file = self.__path_data + "/all_stays.json"
                            stays_bckp_file = self.__path_data + "/all_stays_bckp.json"
                            if os.path.isfile(stays_file):
                                os.rename(stays_file, stays_bckp_file)
                        if test_id in ["TC4"]:  # This test case need to override the fake date to an incorrect checkout day one...
                            frozen_time = datetime(2024, 6, 15, 0, 0, 0)
                            freeze_time(frozen_time).start()
                        hm.guest_checkout(input_data["roomKey"])
                    if test_id in ["TC1"]:
                        self.assertEqual(result.exception.message, "Given SHA256 room_key code is not a valid SHA256 string")
                    if test_id in ["TC2"]:  # Restore stays file name...
                        self.assertEqual(result.exception.message, "Wrong file or file path")
                        if os.path.isfile(stays_bckp_file):
                            os.rename(stays_bckp_file, stays_file)
                    if test_id in ["TC3"]:
                        self.assertEqual(result.exception.message, "Given room_key not found in stays file")
                    if test_id in ["TC4"]:
                        self.assertEqual(result.exception.message, "The departure date was not expected to be today according to the stay information")
                        freeze_time().stop()
                    if test_id in ["TC7"]:
                        self.assertEqual(result.exception.message, "Client already found in checkouts file. Not allowed to checkout again")
        #store_final_hash = self.get_store_hash()
        #self.assertEqual(store_final_hash, store_original_hash)
