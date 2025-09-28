import datetime
import sys  
import re


def get_valid_symbol(Init_Amend, prompt=None):
    

    #print(f"Debug: In get_valid_symbol") #debug
    while True:
        
        try:
            if Init_Amend == "Init":     #print(f"Debug: In get_valid_symbol") #debug
              symbol = input(prompt).strip()  # Remove leading/trailing whitespace
              #print(f"Debug: User entered {symbol}") #debug
            elif Init_Amend == "Amend":
              symbol = input.strip()
              
            if re.match(r'^[A-Za-z]{1,4}$', symbol):
                break
        except Exception as e:
          print("Invalid symbol. Please enter 1-4 letters.")

    return symbol.upper()  # Convert to uppercase for consistency
        

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

def get_valid_call_put  (prompt):    
    # Get valid input for Call or Put option
    while True:
        cp = input("Enter C/P: ").upper()
        if cp == "C" or cp == "P":
            break
        else:
            print("Invalid input. Please enter C or P.")        
    return cp   


def get_valid_status (prompt):
    while True:

        status = input("Enter Status: (O)pen/(C)losed: ").upper()
        if status == "O" or status == "C":
            return status.upper()
            break   
        
        else:
                    print("Invalid input. Please enter (O)pen or (C)losed.")         

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

#def main():      # Example usage

    #get_valid_date("Enter Date (MM-DD-YYYY):")
    get_valid_exp_date("Expiration Date (MM-DD-YYYY); <Enter> for last used: ",default_date="12-31-2023")
    get_valid_symbol("Enter Symbol: ")
    get_valid_call_put("Enter C/P: ")
    get_valid_status ("Enter Status: (O)pen/(C)losed: ")
    get_valid_float("Enter Premium ($x.xx): ",2)
    get_valid_int("Enter Contracts: ")

#f __name__ == "__main__":
  # main()
