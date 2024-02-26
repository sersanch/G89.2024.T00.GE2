"""
THIS MAIN PROGRAM IS ONLY VALID FOR THE FIRST THREE WEEKS OF CLASS
IN GUIDED EXERCISE 2.2, TESTING MUST BE PERFORMED USING UNITTESTS.
"""

import src.main.python.uc3mtravel
from pathlib import Path


def main():
    """
    Gets json input with booking data and sends data for validation...
    """
    mng = src.main.python.uc3mtravel.HotelManager()
    res = mng.new_booking_from_json(str(Path.home()) + "/PycharmProjects/G89.2024.T00.GE2/src/data/bookings/booking_02.json")
    print(str(res))


if __name__ == "__main__":
    main()
