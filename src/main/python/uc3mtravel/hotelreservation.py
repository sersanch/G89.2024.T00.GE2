""" Module that manages the operations for hotel booking transactions... """
import hashlib
from datetime import datetime


class HotelReservation:
    """ Class that manages the operations for hotel booking transactions... """

    def __init__(self, id_card, credit_card_number, name_surname, phone_number, room_type, arrival, num_days):
        """ Constructor of a hotel reservation... """
        self.__credit_card_number = credit_card_number
        self.__id_card = id_card
        self.__name_surname = name_surname
        self.__phone_number = phone_number
        self.__room_type = room_type
        self.__arrival = arrival
        self.__num_days = num_days

    def __str__(self):
        """ Return a json string with the elements required to calculate the localizer """
        # VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number": self.__phone_number,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "arrival": self.__arrival,
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
        return hashlib.md5(self.__str__().encode()).hexdigest()

    @property
    def json(self):
        return {"creditCardNumber": self.__credit_card_number,
                "idCard": self.__id_card,
                "nameSurname": self.__name_surname,
                "phoneNumber": self.__phone_number,
                "roomType": self.__room_type,
                "arrival": self.__arrival,
                "numDays": self.__num_days,
                }
