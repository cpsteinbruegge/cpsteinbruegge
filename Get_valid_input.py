import datetime
import sys  

def get_valid_date(prompt):
    
    while True:
        date_str = input(prompt)
        try:
          #print(f"Debug: User entered {date_str}") #debug

        

          #print(f"Debug: is date_str empty? {'Yes' if not date_str else 'No'}") #debug
          
         #(f"Debug: User entered {date_str}") #debug

          if not date_str:
            #print (f"{datetime.datetime.now().date()}")   # return today's date if no date is entered
            datetoday = datetime.datetime.now().strftime("%m-%d-%Y")
            print(f"{datetoday}")
            return datetoday
            #return datetime.datetime.now.date()   # return today's date if no date is entered
        
          
        
          datetoday = datetime.datetime.strptime(date_str, "%m-%d-%Y")
          print(f"{datetoday.date()}")
          return datetoday.date()
        
        except ValueError:
            print("Invalid date. Please try again.")


#current_date = get_valid_date("Enter Date (MM-DD-YYYY):")
# get_valid_date("Enter Date (MM-DD-YYYY), Press <Return> for today's date: ")
#print(current_date)    # print(current_date)
 

''' def get_valid_date(prompt):
        date_str = input(prompt)
        if not date_str:
            return datetime.date.today()    # return today's date if no date is entered

        try:
            date = datetime.datetime.strptime(date_str, "%m-%d-%Y")
            return date.date()
        except ValueError:
            print("Invalid date. Please try again.") '''

def get_valid_exp_date(prompt, default_date=None):
    while True:
        if default_date:
            prompt_with_default = f"{prompt} (Press <Enter> to use {default_date}): "
        else:
            prompt_with_default = f"{prompt}: "

        date_str = input(prompt_with_default)
        if not date_str:
            if default_date:
                return default_date
            else:
                print("No default date provided. Please enter a valid date.")
                continue

        try:
            date = datetime.datetime.strptime(date_str, "%m-%d-%Y")
            return date.strftime("%m-%d-%Y")
        except ValueError:
            print("Invalid date format. Please try again.")

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

