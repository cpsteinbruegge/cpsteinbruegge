import datetime
import sys  
import re


def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            date = datetime.datetime.strptime(date_str, "%m-%d-%Y")
            return date.date()
        except ValueError:
            print("Invalid date. Please try again.")

def get_valid_float(prompt,decimal_places):
    while True:
        try:
            value = float(input(prompt))

            return round(value, decimal_places)
        
        except ValueError:
            print(f"Invalid input. Please enter a number with {decimal_places} decimal places. ")

def get_valid_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
                
        except ValueError:
            print("Invalid input. Please enter an integer. ")

def get_valid_symbol(prompt):
    while True:
        symbol = input(prompt).upper()
        if re.match("^[a-z,A-Z]{1,4}$", symbol):
            return symbol
        else:
            print("Invalid input. Please enter a symbol with 1 to 4 characters only.")
                

