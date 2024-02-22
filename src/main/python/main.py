"""
THIS MAIN PROGRAM IS ONLY VALID FOR THE FIRST THREE WEEKS OF CLASS
IN GUIDED EXERCISE 2.2, TESTING MUST BE PERFORMED USING UNITTESTS.
"""

import src.main.python.uc3mtravel


def main():
    """
    Gets json input with booking data and sends data for validation...
    """
    mng = src.main.python.UC3MTravel.HotelManager()
    res = mng.read_data_from_json("test.json")
    str_res = str(res)
    print(str_res)
    print("CreditCard: " + res.creditcard)
    print(res.localizer)


if __name__ == "__main__":
    main()
