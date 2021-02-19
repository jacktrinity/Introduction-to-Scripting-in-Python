"""
Project for Week 4 of "Python Programming Essentials".
Collection of functions to process dates.

CodeSkulptor: https://py3.codeskulptor.org/#user305_3IbfquymagUdfjD.py

days_in_month(year, month)
is_valid_date(year, month, day)
days_between(year1, month1, day1, year2, month2, day2)
age_in_days(year, month, day)
"""

import datetime

def days_in_month(year, month):
    """
    Inputs:
      year  - an integer between datetime.MINYEAR and datetime.MAXYEAR
              representing the year
      month - an integer between 1 and 12 representing the month

    Returns:
      The number of days in the input month.
    """
    
    if month == 12:  # If the month is December
        total_days = 31
    else:  # All the other month
        total = datetime.date(year, month + 1, 1) - datetime.date(year, month, 1)
        total_days = total.days
    
    return total_days

def is_valid_date(year, month, day):
    """
    Inputs:
      year  - an integer representing the year
      month - an integer representing the month
      day   - an integer representing the day

    Returns:
      True if year-month-day is a valid date and
      False otherwise
    """
    
    if (datetime.MINYEAR <= year <= datetime.MAXYEAR) and (1 <= month <= 12):
        if 1 <= day <= days_in_month(year, month):
            return True
        else:
            return False
    else:
        return False

def days_between(year1, month1, day1, year2, month2, day2):
    """
    Inputs:
      year1  - an integer representing the year of the first date
      month1 - an integer representing the month of the first date
      day1   - an integer representing the day of the first date
      year2  - an integer representing the year of the second date
      month2 - an integer representing the month of the second date
      day2   - an integer representing the day of the second date

    Returns:
      The number of days from the first date to the second date.
      Returns 0 if either date is invalid or the second date is
      before the first date.
    """
    if (is_valid_date(year1, month1, day1)) and (is_valid_date(year2, month2, day2)):
        
        first_datetime = datetime.date(year1, month1, day1)
        second_datetime = datetime.date(year2, month2, day2)
        
        if first_datetime < second_datetime:
            date_difference = second_datetime - first_datetime
            
            return date_difference.days
        else:
            return 0
    else:
        return 0

def age_in_days(year, month, day):
    """
    Inputs:
      year  - an integer representing the birthday year
      month - an integer representing the birthday month
      day   - an integer representing the birthday day

    Returns:
      The age of a person with the input birthday as of today.
      Returns 0 if the input date is invalid or if the input
      date is in the future.
    """
    
    if is_valid_date(year, month, day):
        today = datetime.date.today()
        birthday = datetime.date(year, month, day)
        
        if today > birthday:
            date_difference = today - birthday
            age = date_difference.days
            
            return age
        else:
            return 0
        
    else:
        return 0

