"""
THIS MAIN PROGRAM IS ONLY VALID FOR THE FIRST THREE WEEKS OF CLASS
IN GUIDED EXERCISE 2.2, TESTING MUST BE PERFORMED USING UNITTESTS.
"""

import src.main.python.uc3mtravel


def main():
    """
    Gets json input with booking data and sends data for validation...
    """
    mng = src.main.python.uc3mtravel.HotelManager()
    res = mng.room_reservation("./data/bookings/booking_01.json")
    print(str(res))


if __name__ == "__main__":
    main()
