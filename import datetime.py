import datetime
import os
import sys
import time
def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        if not date_str:
            date = datetime.datetime.now().date()   # return today's date if no date is entered
            return date     
        try:
            date = datetime.datetime.strptime(date_str, "%m-%d-%Y")
            return date.date()
        except ValueError:
            print("Invalid date. Please try again.")


current_date = get_valid_date("Enter Date (MM-DD-YYYY):")
# get_valid_date("Enter Date (MM-DD-YYYY), Press <Return> for today's date: ")
print(current_date)    # print(current_date)
 