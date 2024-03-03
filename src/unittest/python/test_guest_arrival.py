""" Module that includes the tests of GE2.2 - Function 2 - Guest Arrival """
import unittest
import os.path
import json
from pathlib import Path
from freezegun import freeze_time
from uc3mtravel import HotelManager
from uc3mtravel import HotelManagementException


class TestGuestArrival(unittest.TestCase):
    """ Class to test Function 2: guest arrival process """

    __path_tests = str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/data/tests/"
    __path_data = str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/data/"
    __tmp_test_data_file = "tmp_test_data.json"

    @classmethod
    def setUpClass(cls):
        """ Opens input test file with test data and assigns to attributes for the tests to use. Also clear store..."""
        # Load all tests...
        lines = []
        try:
            with open(cls.__path_tests + "f2_tests.txt", encoding='UTF-8', mode="r") as file:
                for line in file:
                    lines.append(line.strip())
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        cls.__test_data_f2 = lines
        # Clear the stays file from possible previous runs...
        all_stays = cls.__path_data + "/all_stays.json"
        if os.path.isfile(all_stays):
            os.remove(all_stays)
        return True

    def generate_tmp_test_data_file(self, line):
        """ Generates an individual test file with just on entry to test as F2 requires a file path as input..."""
        with open(self.__path_tests + self.__tmp_test_data_file, encoding="UTF-8", mode="w") as file:
            file.write(line)

    @freeze_time("2024-06-14")
    def test_guest_arrival_tests_ok(self):
        """ TestCases: TC1, TC62, TC63 - Expected OK. Checks File and Data. Hash SHA-256 OK + Stay is stored """
        for index, input_data in enumerate(self.__test_data_f2):
            if index + 1 in [1, 62, 63]:  # TC1, TC62, TC63 are ok tests...
                test_id = "TC" + str(index + 1)
                with self.subTest(test_id):
                    print("Executing: " + test_id + ": " + input_data)
                    self.generate_tmp_test_data_file(input_data)
                    hm = HotelManager()
                    room_key = hm.guest_arrival(self.__path_tests + self.__tmp_test_data_file)
                    match test_id:
                        case "TC1":
                            self.assertEqual(room_key, "ee25b7b863b77e9106d851875103a3076748a0d487e7a42340ea18855d36b89f")
                        case "TC62":
                            self.assertEqual(room_key, "6cfe66d06630a99766b9fb87c5a09f4707d60a95212a45c1edd2c6fba334c2c0")
                        case "TC63":
                            self.assertEqual(room_key, "8dd164818a021e709aec4ed512be4318b16d3fc94c78579271e91a1991db870e")
                    try:
                        with open(self.__path_data + "/all_stays.json", encoding='UTF-8', mode="r") as f:
                            stays = json.load(f)
                    except FileNotFoundError as e:
                        raise HotelManagementException("Wrong file or file path") from e
                    except json.JSONDecodeError:
                        stays = []
                    stay_found = False
                    for stay in stays:
                        if stay["idCard"] == json.loads(input_data)["IdCard"]:
                            stay_found = True
                    self.assertTrue(stay_found)

    def test_guest_arrival_tests_ko(self):
        """ TestCases: TC2 to TC23 -  Expected KO. Deletion of nodes...
                       TC24 to TC45 - Expected KO. Duplication of nodes...
                       TC46 to TC61 - Expected KO. Modification of nodes... """
        for index, input_data in enumerate(self.__test_data_f2):
            if index + 1 not in [1, 62, 63]:  # TC1 is the first in the file and only one ok...
                test_id = "TC" + str(index + 1)
                with self.subTest(test_id):
                    print("Executing: " + test_id + ": " + input_data)
                    self.generate_tmp_test_data_file(input_data)
                    hm = HotelManager()
                    with self.assertRaises(HotelManagementException) as result:
                        room_key = hm.guest_arrival(self.__path_tests + self.__tmp_test_data_file)
                        # Not all invalid tests will raise json format error because error may be in data or labels...
                        if test_id not in ["TC1", "TC62", "TC63", "TC13", "TC16", "TC19", "TC22", "TC35", "TC38", "TC41", "TC44", "TC51", "TC54", "TC57", "TC60"]:
                            self.assertEqual(result.exception.message, "Input data file is not a correct json format as expected")
                        if test_id in ["TC13", "TC19", "TC35", "TC41", "TC51", "TC57"]:
                            self.assertEqual(result.exception.message, "Input data file is not a correct json format: incorrect key values")
                        if test_id in ["TC16", "TC22", "TC38", "TC44", "TC54", "TC60"]:
                            self.assertEqual(result.exception.message, "No reservation was found with the provided localizer and id card")
