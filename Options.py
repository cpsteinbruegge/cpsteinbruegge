import math
import json
import csv
import os
import datetime
import sys

    #print(f"Current working directory: {os.getcwd()}")  #debugging line
    #print(f"Python module search path: {sys.path}")  #debugging line
    #print("\n".join(sys.path))  #debugging line


import tabulate
import Get_valid_input
import re


#import Get_ticker_symbol




last_exp_date = None
class Options:
    def __init__(self,file_name):
        self.file_name = file_name

        try:
            if not os.path.exists(self.file_name):
                with open(self.file_name, 'w', newline="") as file:
                  writer = csv.writer(file)
                  writer.writerow(["Symbol" ,"Date","C/P","Strike","Exp Date","Premium","Contracts", "Total Open Premium","Current Price","Close Cost", "Status", "Profit/Loss"])
            #debugging line
                
            with open(self.file_name, 'r', newline="") as file:
              reader = csv.reader(file)
              data = [row for row in reader if row]
              if data:
                  print("Header row: ",data[0])  
              print("All rows: ",data)   #debugging line

        except Exception as e:
            print(f"Error initializing CSV file: {e}")
            sys.exit(1)

   


    def choose_option(self):
        #debug 
        print("Made it to Options Tracker\n")
        while True:

            print("\nOptions Tracker\n")

            print("1. Enter new trade")
            print("2. View trades")
            print("3. Calculate Total Profit/Loss")
            print("4. Amend trade records")
            print("5. Delete trade records")
            print("6. Exit")
            print("\n")
         
            choice = input("Enter choice: ").strip()

            print("\n")
         
            if choice == "1":
                self.enter_data()
            elif choice == "2":
                print
                self.view_trades()
            elif choice == "3":
                self.calculate_total_profit_loss()
            elif choice == "4":
                print("To be implemented") #Delete trade records
                # Amend or delete trade records
                
                Amend_delete = "A" #Delete trade records
                Options_Trade_Editor(self.file_name, Amend_delete)  
                # os.remove(self.file_name) 
            elif choice == "5":
                Amend_delete = "D" #Delete trade records
                Options_Trade_Editor(self.file_name, Amend_delete) #Amend trade records  
                # os.remove(self.file_name) 
            elif choice == "6":
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

 
    

    def enter_data(self):  
        global last_exp_date     
        
        proceed = True                                  
                
        while proceed:
            #debug
            print("Made it to enter_data") #debug

            #symbol =self.get_valid_symbol("Enter Symbol: ") 
            #debug    
            #tradedate = Get_valid_input.get_valid_date("Open Date (MM-DD-YYYY); <Enter> for today's date:")    
            
           
            # Create a dictonary data object for the trade record
           
            #debug
            #print(f"Debug: User entered {symbol}") #debug
            tradedate = Get_valid_input.get_valid_date("Open Date (MM-DD-YYYY); <Enter> for today's date:")
            symbol = Get_valid_input.get_valid_symbol("Enter Symbol: ")
            strike = Get_valid_input.get_valid_int("Enter Strike: ")
            exp_date = Get_valid_input.get_valid_exp_date("Expiration Date (MM-DD-YYYY); <Enter> for last used: ", default_date=last_exp_date)
            last_exp_date = exp_date
            premium = Get_valid_input.get_valid_float("Enter Premium ($x.xx): ", 2)
            contracts = Get_valid_input.get_valid_int("Enter Contracts: ")
            current_price = Get_valid_input.get_valid_int("Enter Current Price: ")
            close_cost = Get_valid_input.get_valid_int("Enter Close Cost: ")
            status = Get_valid_input.get_valid_status("Enter Status (Open/Closed): ")
            cp = Get_valid_input.get_valid_call_put("Enter C/P: ")

            trade_record = {
                "symbol": symbol,
                "tradedate": tradedate,
                "strike": strike,
                "exp_date": exp_date,
                "premium": premium,
                "contracts": contracts,
                "current_price": current_price,
                "close_cost": close_cost,
                "status": status,
                "cp": cp
            }
             
             # Log the trade
            self.log_trade(
            trade_record["symbol"],
            trade_record["tradedate"],
            trade_record["cp"],
            trade_record["strike"],
            trade_record["exp_date"],
            trade_record["premium"],
            trade_record["contracts"],
            trade_record["current_price"],
            trade_record["close_cost"],
            trade_record["status"]
        )
            last_exp_date = trade_record["exp_date"]  # Update last expiration date

             
            #self.log_trade(symbol,tradedate, cp, strike, exp_date, premium, contracts, current_price, close_cost, status)
            
            #Ask user if they want to add another trade

            while True:   
               answer = input("Add another trade? Y/N ").upper()   
               if answer in {'Y','N'}:
                   break
               else:
                   print("Invalid input. Please enter Y or N.")

            if answer == "N":
                    proceed = False  
                    self.view_trades()  # Display the updated trades after amendment



            elif answer == "Y":
                 proceed = True           
              
    def log_trade (self,symbol, tradedate, cp, strike, exp_date, premium, contracts, current_price, close_cost, status,):
        try:
            total_open_premium= float(premium) * int(contracts) * 100
            profit_loss = int(total_open_premium - close_cost)
            with open(self.file_name, mode='a',newline= "") as file:
                writer = csv.writer(file)
                writer.writerow([symbol, tradedate, cp, strike, exp_date, premium, contracts, f"{total_open_premium:.0f}" , int(current_price), close_cost, status, int(profit_loss)])
        except Exception as e:
            print(f"Error logging trade: {e}")
            sys.exit(1)
        

    def view_trades(self):
        print(f"File exists: {os.path.exists(self.file_name)}")  #debugging line
        
        print("\n")

        try:
            if not os.path.exists(self.file_name):
                  print("No trade records found.")
                  return
            with open(self.file_name , mode='r') as file:
                #debugging line
                print("Raw data from file: ",file.read())

            with open(self.file_name , mode='r') as file:  
                reader = csv.reader(file)
                data = [row for row in reader if row]  #Skip empty rows
                #data = list(reader) reader = csv.reader(file)
               
                # print("DATA READ FROM FILE", data)  Debug
                if data:
                    print(data[0])  #debugging line for header row
                    #print("All rows: ",data)  #debugging line
                    print("All rows: ",data)  #debugging line
            if len(data) > 1:
               headers =  ["Row"] + data[0] 
               rows = [[i] + row for i,row in enumerate(data[1:], start=1) if row] 
               print("\n")
               print(tabulate.tabulate(rows, headers=headers,tablefmt='PIPE'))   
               #debugging line
               print("Total Rows: ",rows,len(rows))  #debugging line
               return rows            
               
            else:
                print("No trade records found.")

        except Exception as e:
            print(f"Error viewing trades: {e}")
            sys.exit(1)  

    def calculate_total_profit_loss(self):
        try:
            with open(self.file_name, mode='r') as file:
                reader = csv.reader(file)
                data = [row for row in reader if row]  #Skip empty rows
                
            if len (data) == 1:
                    print("No trade records found.")
                    return
            
            total_profit_loss = 0
            for row in data[1:]:
                    try:
                        total_profit_loss += int(row[-1])
                    except (ValueError, IndexError):
                        print(f"Error calculating profit/loss for row {row}; skipping.")
                        #debug
                        print("Row", row)
            print(f"Total Profit/Loss: {total_profit_loss}")
        except Exception as e:
            print(f"Error calculating profit/loss: {e}")
            sys.exit(1)

def Options_Trade_Editor (file_name, Amend_delete):
    print("Made it to Options_Trade_Editor") #debugging line
            #debugging line
            #        print("Made it to Options_Trade_Editor") #debugging line
            #   # Check if the file exists
    if not os.path.exists(file_name):   
        print(f"File {file_name} does not exist.")
        return  
    # Exit the function if the file does not exist
    # If the file exists, proceed with the Options class            
    Options_Editor = Options(file_name)

    # Initialize Options class with the file name
    Options_Editor.view_trades()  
    rows = Options_Editor.view_trades()  # Get the current trades from the file     

     # Display the current trades in the file

    #Ask Amend or Delete trade records
   
    # Amend trade records

    if Amend_delete == "A":
        # Ask for the trade row to amend
        trade_row = Get_valid_input.get_valid_int ("Enter the trade row to amend: ")    
        #Display the current trade details
        if 1 <= trade_row <= len(rows): 
            print("/n")
            #print("Amend Trade, not yet implemented.")              
            print(f"Current trade details: {rows[trade_row-1]}")
            
            #Make sure inputs are valid

            field_mapping = {
            "Symbol": Get_valid_input.get_valid_symbol,
            "Date": Get_valid_input.get_valid_date,
            "C/P": Get_valid_input.get_valid_call_put,
            "Strike": Get_valid_input.get_valid_int,
            "Exp Date": Get_valid_input.get_valid_exp_date,
            "Premium": Get_valid_input.get_valid_float,
            "Contracts": Get_valid_input.get_valid_int,
            "Total Open Premium": Get_valid_input.get_valid_float,  # Optional: Recalculate instead of asking
            "Current Price": Get_valid_input.get_valid_int,
            "Close Cost": Get_valid_input.get_valid_int,
            "Status": Get_valid_input.get_valid_status,
            "Profit/Loss": Get_valid_input.get_valid_float,  # Optional: Recalculate instead of asking
        }

        #Start getting new data and update rows

        # Header row for reference
            headers = ["Symbol", "Date", "C/P", "Strike", "Exp Date", "Premium", "Contracts",
                   "Total Open Premium", "Current Price", "Close Cost", "Status", "Profit/Loss"]

        # Update the row
            updated_row = []
        #debugging line

            print("Editing trade details:")
            print(list(enumerate(zip(headers, rows[trade_row-1]), start=1)))  #debugging line
               
        

        #
        # Loop through each field and ask for new values

            for i, (header, value) in enumerate(zip(headers, rows[trade_row-1][1:])):   # Skip the first column (row number)
                print(f"Editing Field: {header} (Current Value: {value})")
                validation_method = field_mapping.get(header)  # Get the corresponding validation method
                if validation_method:
                    new_value = input(f"Enter new value for {header} (or press Enter to keep '{value}'): ").strip()
                    if new_value:
                    # Validate the new value using the corresponding method
                        try:
                            validated_value = validation_method(f"Enter valid {header}: ")
                            updated_row.append(validated_value)
                            print(f"Debug - Updated {header} to {validated_value}")  #debugging line
                        except Exception as e:
                            print(f"Invalid input for {header}. Keeping original value: {value}")
                            updated_row.append(value)
                    else:
                    # Keep the original value if no input is provided
                        print(f"No input provided for {header}. Keeping original value: {value}",end="")  #debugging line
                        updated_row.append(value)
                        print(f"Keeping original value for {header}: {value}")
                else:
                # If no validation method is defined, keep the original value
                        updated_row.append(value)

           # Update the row in the list
                rows[trade_row - 1] = updated_row
                print(f"Updated trade details: {rows[trade_row - 1]}",end="")  #debugging line
            

        # Save the updated rows back to the file
            try:
                with open(file_name, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)  # Write the header row
                    writer.writerows(rows)  # Write all rows
                    print("File updated successfully.")
                    Options_Editor.view_trades()  # Display the updated trades after amendment


            except Exception as e:
                print(f"Error updating file: {e}")
                sys.exit(1)
        else:
          print(f"Trade {trade_row} not found.")

    

    if Amend_delete == "D":  
         
        # Ask for the trade row to delete
        trade_row = Get_valid_input.get_valid_int ("Enter the trade row to delete: ")
        # Check if the trade ID exists in the file
        if 1 <= trade_row <= len(rows): 
            # Delete the trade from the file
            del rows[trade_row-1]  # Adjust for zero-based index
            print(f"Trade {trade_row} deleted successfully.")

            try:        #Save the changes to the file
                with open(file_name, "w", newline="") as file:
                 writer = csv.writer(file)
                    
                   # Write the header row first
                 writer.writerow(["Symbol", "Date", "C/P", "Strike", "Exp Date", "Premium", "Contracts", "Total Open Premium", "Current Price", "Close Cost", "Status", "Profit/Loss"])  

                 writer.writerows([row[1:] for row in rows])  # Write all rows except the header

                 print(f"File exists: {os.path.exists(file_name)}")  #d #debug
                     #debugging line            
                print("File contents after deletion:")
                with open(file_name, "r") as file:
                    print(file.read())  # Print the contents of the file after deletion 
                #print(f"File {file_name} updated successfully.")

                Options_Editor.view_trades()  # Display the updated trades after deletion
            except Exception as e:
                print(f"Error updating file: {e}")
                sys.exit(1)

        else:
            print(f"Trade {trade_row} not found.") 

def main():
    try:
        #debugging line
        print("Made it to main") #debugging line
        print(f"Current working directory: {os.getcwd()}")  #debugging line

    except Exception as e:
        print(f"Error in main: {e}")
        sys.exit(1)    
    

    file_name = "Options.csv"
    
    OptionsTracker = Options(file_name)
    OptionsTracker.choose_option()
    



if __name__ == "__main__":
    main()
