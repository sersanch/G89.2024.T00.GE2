""" Main module to manage hotel operations. Includes the exposed methods... """
import json
import re
import os
from datetime import datetime
from pathlib import Path
import luhn
from .hotelreservation import HotelReservation
from .hotelmanagementexception import HotelManagementException


class HotelManager:
    """ Main class to manage hotel operations. Includes the exposed methods... """

    def __init__(self):
        self.__path_data = str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/data/"

    def read_data_from_json(self, fi, mode):
        """ Opens input json file with data of the booking, checks formats and returns data... """
        try:
            with open(fi, encoding='UTF-8', mode=mode) as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError:
            data = []
        return data

    def write_data_to_json(self, fi, data, mode):
        """ Opens output json file and dumps data with bookings... """
        try:
            with open(fi, encoding='UTF-8', mode=mode) as f:
                json.dump(data, f, indent=4)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from e
        return data

    def validate_credit_card(self, credit_card_number):
        """ Validates the credit card number according to the luhn algorithm """
        if not str(credit_card_number).isdigit():
            return False
        if len(str(credit_card_number)) != 16:
            return False
        return luhn.verify(credit_card_number)

    def validate_name_surname(self, name_surname):
        """ Validates the name and surname.
            Between 10 and 50 characters with at least two strings separated by white space """
        if len(name_surname) < 10 or len(name_surname) > 50:
            return False
        if len(re.findall(r'\S+', name_surname)) < 2:
            return False
        return True

    def validate_phone_number(self, phone_number):
        """ Validates the phone number. Valid phone number (9 digits) """
        return len(str(phone_number)) == 9 and str(phone_number).isdigit()

    def validate_room_type(self, room_type):
        """ Validates the room type.
            The room type can take one of the following values: single, double or suite """
        return room_type in ('single', 'double', 'suite', 'SINGLE', 'DOUBLE', 'SUITE')

    def validate_arrival(self, arrival):
        """ Validates the arrival date.
            Date of arrival at the hotel, in the format "DD/MM/YYYY" (example (01/07/2024) """
        try:
            datetime.strptime(arrival, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    def validate_num_days(self, num_days):
        """ Validates the arrival date. A value between 1 and 10 """
        return str(num_days).isdigit() and (1 <= int(num_days) <= 10)

    def room_reservation(self, credit_card, id_card, name_surname, phone_number, room_type, arrival, num_days):
        """ HM-FR-01: Register a room reservation. Receive booking info and return a code to enter the room """

        # Check formats and validity...
        if not self.validate_credit_card(credit_card):
            raise HotelManagementException("Invalid credit card number provided")
        if not self.validate_name_surname(name_surname):
            raise HotelManagementException("Invalid name surname provided (must be name and surname separated)")
        if not self.validate_phone_number(phone_number):
            raise HotelManagementException("Invalid phone number provided (must be 9 digits)")
        if not self.validate_room_type(room_type):
            raise HotelManagementException("Invalid room type provided (must be single, double or suite")
        if not self.validate_arrival(arrival):
            raise HotelManagementException("Invalid arrival date provided (format must be dd/mm/yyyy")
        if not self.validate_num_days(num_days):
            raise HotelManagementException("Invalid number of days provided (must be between 1 and 10)")

        # Create object HotelReservation...

        reservation = HotelReservation(id_card=id_card, credit_card_number=credit_card,
                                       name_surname=name_surname, phone_number=phone_number,
                                       room_type=room_type, arrival=arrival, num_days=num_days)

        # Get localizer and store information of reservation in reservations file for further processing...

        booking_data = reservation.json
        booking_data["localizer"] = reservation.localizer

        # Save to bookings file. Before saving to the file we check that the client does not have another booking...

        path_file_bookings = self.__path_data + "all_bookings.json"

        all_bookings = []
        if os.path.isfile(path_file_bookings):
            all_bookings = self.read_data_from_json(path_file_bookings, "r")

        for booking in all_bookings:
            if booking["idCard"] == booking_data["idCard"]:
                raise HotelManagementException("Client already has a reservation")

        all_bookings.append(booking_data)
        self.write_data_to_json(path_file_bookings, all_bookings, "w")

        return booking_data["localizer"]
