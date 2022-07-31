#!/usr/bin/env python3
"""Calculate the number of days between two dates.

Title:
Number of Days

Description:
Your program should take two string inputs from the user
in the format (dd/mm/yyyy)
and calculate the number of days between those two dates.
Submitted by Kanishk
"""
DAYS_IN_A_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def number_of_days(date1: str, date2: str) -> int:
    """Return the number of days between two dates."""
    if date1 == date2:
        return 0
    days_between = 0
    day1, month1, year1 = _parse_date(date1)
    day2, month2, year2 = _parse_date(date2)

    if year1 > year2:
        year = year2
        while year < year1:
            # check for leap years
            if year % 4 == 0:
                if year % 100 == 0 and year % 400 != 0:
                    days_between += 365
                else:
                    days_between += 366
            else:
                days_between += 365
            year += 1
        if month1 > month2:
            months_between = [month for month in range(0, 13)
                              if month1 > month >= month2]
            days_between += sum([DAYS_IN_A_MONTH[month]
                                 for month in months_between])
        elif month2 > month1:
            months_between = [month for month in range(0, 13)
                              if month2 > month >= month1]
            days_between -= sum([DAYS_IN_A_MONTH[month]
                                 for month in months_between])
        days_between += day1 - day2
    elif year2 > year1:
        year = year1
        while year < year2:
            # check for leap years
            if year % 4 == 0:
                if year % 100 == 0 and year % 400 != 0:
                    days_between += 365
                else:
                    days_between += 366
            else:
                days_between += 365
            year += 1
        if month2 > month1:
            months_between = [month for month in range(0, 13)
                              if month2 > month >= month1]
            days_between += sum([DAYS_IN_A_MONTH[month]
                                 for month in months_between])
        elif month1 > month2:
            months_between = [month for month in range(0, 13)
                              if month1 > month >= month2]
            days_between -= sum([DAYS_IN_A_MONTH[month]
                                 for month in months_between])
        days_between += day2 - day1
    else:
        if month1 > month2:
            months_between = [month for month in range(0, 13)
                              if month1 > month >= month2]
            days_between += sum([DAYS_IN_A_MONTH[month]
                                 for month in months_between])
            # check for leap month in a leap year (every fourth February)
            if 2 in months_between and year1 % 4 == 0:
                if year1 % 100 == 0 and year1 % 400 != 0:
                    pass
                else:
                    days_between += 1
            days_between += day1 - day2
        elif month2 > month1:
            months_between = [month for month in range(0, 13)
                              if month2 > month >= month1]
            days_between += sum([DAYS_IN_A_MONTH[month]
                                 for month in months_between])
            # check for leap month in a leap year (every fourth February)
            if 2 in months_between and year1 % 4 == 0:
                if year1 % 100 == 0 and year1 % 400 != 0:
                    pass
                else:
                    days_between += 1
            days_between += day2 - day1
        else:
            days_between += max(day1, day2) - min(day1, day2)

    return days_between


def _parse_date(date: str) -> tuple:
    """Return date as a tuple of ints in the format (D, M, Y)."""
    date_split = date.split("/")
    return int(date_split[0]), int(date_split[1]), int(date_split[2])


def _start():
    """Start program interactively."""
    date1 = input("Please type in the first date: ")
    date2 = input("Please type in the second date: ")

    print(f"The number of days between {date1} and {date2} "
          f"is {number_of_days(date1, date2)}.")


if __name__ == "__main__":
    _start()
