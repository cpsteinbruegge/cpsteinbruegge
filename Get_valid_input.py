import datetime
import sys  
import re
import msvcrt
import keyboard


#def get_single_key():


    # Waits for a single key press
    # Suppress the key press event
    # This will block until a key is pressed

    
 #   key = keyboard.read_event(suppress=True).name     # Waits for a single key press

  #  return key

#def ms_get_single_key():

  #  key = msvcrt.getch()  # Waits for a single key press
   # return key.decode()  # Decode the byte to a string

#Exit and return to main program if input is 'X' or 'x'

class RestartProgram(Exception):
    pass

def validate_symbol(value):
    if re.match(r'^[A-Za-z]{1,4}$', value):
        return value.upper()
     
    else:
        raise ValueError("Invalid symbol format. Please enter 1-4 letters.")


def get_valid_symbol(prompt):
    #print(f"Debug: In get_valid_symbol") #debug
    while True:
        
        try:


            symbol = input(prompt).strip()  # Remove leading/trailing whitespace
            #print(f"Debug: User entered {symbol}") #debug
            if symbol.upper() == 'X' or symbol.lower() == 'x':
                print("Exiting program.")
                raise RestartProgram()
            if re.match(r'^[A-Za-z]{1,4}$', symbol):
                break
            else:
                print("Invalid symbol. Please enter 1-4 letters.")

        except RestartProgram:
          raise     
       
    return symbol.upper()  # Convert to uppercase for consistency
        

def validate_date(value):
     # Accept MM-DD-YYYY or MM/DD/YYYY
    if re.fullmatch(r"\d{2}[-/]\d{2}[-/]\d{4}", value):
        return value
    else:
        raise ValueError("Invalid date format. Please enter as MM-DD-YYYY or MM/DD/YYYY.")
    

def get_valid_date(prompt):
    
    while True:
      try:  
        value = input(prompt).strip()  # Remove leading/trailing whitespace
        if value.upper() == 'X' or value.lower() == 'x':
            print("Exiting program.")
            raise RestartProgram()
        elif not value:
            # If no input, return today's date
            today = datetime.datetime.now().strftime("%m-%d-%Y")
            print(f"Using today's date: {today}")
            return today
        
        elif re.fullmatch(r"\d{2}[-/]\d{2}[-/]\d{4}", value):
            return value.replace('/', '-')  # Normalize to MM-DD-YYYY format
          
           
          #print(f"Debug: User entered {date_str}") #debug

           #try:
          #print(f"Debug: is date_str empty? {'Yes' if not date_str else 'No'}") #debug
          # (f"Debug: User entered {date_str}") #debug
          #    date_str = value.strip()  # Remove leading/trailing whitespace

        #   datetoday = datetime.datetime.strptime(date_str, "%m-%d-%Y")
        #      print(f"{datetoday.date()}")
      except Exception as e:
            print("Invalid date format. Please use MM-DD-YYYY.")   
            continue
        # If the date is valid, return it in MM-DD-YYYY format
                #print(f"Debug: Parsed date is {datetoday.date()}") #debug
                #print(f"Debug: Returning date {datetoday.date()}") #debug        
      except RestartProgram:
          raise
      except Exception as e:
            print(f"Error: {e}. Please try again.")
            continue

        
      
      

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

        if date_str.upper() == 'X' or date_str.lower() == 'x':
            print("Exiting program.")
            raise RestartProgram()
        
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

        if cp.upper() == 'X' or cp.lower() == 'x':
            print("Exiting program.")
            raise RestartProgram()
        
        if cp == "C" or cp == "P":
            break
        else:
            print("Invalid input. Please enter C or P.")        
    return cp   


def get_valid_status (prompt):
    while True:

        status = input("Enter Status: (O)pen/(C)losed: ").upper()

        if status.upper() == 'X' or status.lower() == 'x':
            print("Exiting program.")
            raise RestartProgram()
        
        if status == "O" or status == "C":
            return status.upper()
            break   
        
        else:
                    print("Invalid input. Please enter (O)pen or (C)losed.")     

def validate_float(value, decimal_places=2):
    try:
        float_value = float(value)
        return round(float_value, decimal_places)
    except ValueError:
        return None

def get_valid_float(prompt,decimal_places=2):
    while True:
         value = input(prompt)

        

         if value.upper() == 'X' or value.lower() == 'x':
                print("Exiting program.")
                raise RestartProgram() 
         try:
          return round(float(value), decimal_places)

          #return f"{returnvalue:.{decimal_places}f}"  # Return as string formatted to specified decimal places

         except ValueError:
            print(f"Invalid input. Please enter a number with {decimal_places} decimal places. ")

def validate_int(value):
    try:
        int_value = int(value)
        return int_value
    except ValueError:
        return None

def get_valid_int(prompt):
    while True:
        try:
            value = input(prompt).strip()
            if value.upper() == 'X' or value.lower() == 'x':
                print("Exiting program.")
                raise RestartProgram()
            
            value = int(value)
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
