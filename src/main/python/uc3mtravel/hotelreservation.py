""" Module that manages the operations for hotel booking transactions... """
import hashlib
from datetime import datetime


class HotelReservation:
    """ Class that manages the operations for hotel booking transactions... """

    def __init__(self, id_card, credit_card_number, name_surname, phone_number, room_type, num_days):
        """ Constructor of a hotel reservation...
        :param id_card: personal id card number
        :param credit_card_number: credit card number used for the booking
        :param name_surname: name and surname of the visitor
        :param phone_number: phone number of the visitor
        :param room_type: room type (single, double, suite)
        :param num_days: number of nights for the stay
        """
        self.__credit_card_number = credit_card_number
        self.__id_card = id_card
        justnow = datetime.utcnow()
        self.__arrival = datetime.timestamp(justnow)
        self.__name_surname = name_surname
        self.__phone_number = phone_number
        self.__room_type = room_type
        self.__num_days = num_days

    def __str__(self):
        """ Return a json string with the elements required to calculate the localizer """
        # VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()

    @property
    def creditcard(self):
        """ Getter for credit card number """
        return self.__credit_card_number

    @creditcard.setter
    def creditcard(self, value):
        self.__credit_card_number = value

    @property
    def idcard(self):
        """ Getter for id card number """
        return self.__id_card

    @idcard.setter
    def idcard(self, value):
        self.__id_card = value

    @property
    def localizer(self):
        """ Returns the md5 signature """
        return hashlib.md5(str().encode()).hexdigest()
