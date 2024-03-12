""" Module that manages the operations during the stay of a visitor... """

from datetime import datetime, timedelta
import hashlib


class HotelStay:
    """ Manages the operations during the stay of a visitor... """

    def __init__(self, id_card, localizer, num_days, room_type):
        self.__alg = "SHA-256"
        self.__type = room_type
        self.__id_card = id_card
        self.__localizer = localizer
        justnow = datetime.utcnow()
        self.__arrival = justnow
        # timestamp is represented in seconds.milliseconds
        # to add the number of days we must express it in seconds
        self.__departure = self.__arrival + timedelta(days=int(num_days))

    def __signature_string(self):
        """ Composes the string to be used to generate the room keys """
        arrival = str(self.__arrival)
        departure = str(self.__departure)
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",localizer:" + self.__localizer + ",arrival:" + arrival + ",departure:" + departure + "}"

    @property
    def idcard(self):
        """ Property that represents the product_id of the patient """
        return self.__id_card

    @idcard.setter
    def idcard(self, value):
        self.__id_card = value

    @property
    def localizer(self):
        """ Property that represents the order_id """
        return self.__localizer

    @localizer.setter
    def localizer(self, value):
        self.__localizer = value

    @property
    def arrival(self):
        """ Property that represents the phone number of the client """
        return self.__arrival

    @property
    def room_key(self):
        """ Returns the sha256 signature of the date """
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def departure(self):
        """ Returns the issued at value """
        return self.__departure

    @departure.setter
    def departure(self, value):
        self.__departure = value

    @property
    def json(self):
        """ Returns class info in json format..."""
        return {"alg": self.__alg,
                "idCard": self.__id_card,
                "localizer": self.__localizer,
                "roomType": self.__type,
                "arrival": str(self.__arrival),
                "departure": str(self.__departure)
                }
