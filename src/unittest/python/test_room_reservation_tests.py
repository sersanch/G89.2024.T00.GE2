import unittest
import json
from pathlib import Path
from unittest import TestCase
from uc3mtravel import HotelManager
from uc3mtravel import HotelManagementException


class TestRoomReservation(TestCase):
    """ Class to test room reservation process """

    def setUp(self):
        """ Opens input test files with test data... """
        try:
            with open(str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/testdata/f1_test_credit_card_number"
                                         ".json", encoding='UTF-8', mode="r") as f:
                data_credit_card = json.load(f)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError:
            data_credit_card = []
        self.__data_credit_card = data_credit_card
        return True

    def test_credit_card_number_tc1(self):
        """ TestCase1: TC1. Expected OK: Localizer OK + Booking stored """
        for input_data in self.__data_credit_card:
            if input_data["idTest"] == "TC1":
                hm = HotelManager()
                localizer = hm.room_reservation(input_data["creditCardNumber"], input_data["idCard"],
                                                input_data["nameSurname"], input_data["phoneNumber"],
                                                input_data["roomType"], input_data["arrival"],
                                                input_data["numDays"])
                return self.assertEqual(localizer, "d41d8cd98f00b204e9800998ecf8427e")  # add assertion here
