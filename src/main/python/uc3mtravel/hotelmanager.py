"""
Main class to manage hotel operations. Includes the exposed methods...
"""
import json
from .hotelreservation import HotelReservation
from .hotelmanagementexception import HotelManagementException


class HotelManager:
    """
    Main class to manage hotel operations. Includes the exposed methods..
    """
    def __init__(self):
        pass

    def validate_credit_card(self, x):
        """
        Validates the credit card number...
        :param x: credit card number
        :return: true in case CCN is Ok, false otherwise
        """
        return True

    def read_data_from_json(self, fi):
        """
        Opens input json file with data of the booking...
        :param fi: file name
        :return: data inside in json format or exception
        """
        try:
            with open(fi, encoding='UTF-8') as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from e

        try:
            c = data["CreditCard"]
            p = data["phoneNumber"]
            req = HotelReservation(id_card="12345678Z",
                                   credit_card_number=c,
                                   name_surname="John Doe",
                                   phone_number=p,
                                   room_type="single", num_days=3)
        except KeyError as e:
            raise HotelManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.validate_credit_card(c):
            raise HotelManagementException("Invalid credit card number")

        # Close the file
        return req
