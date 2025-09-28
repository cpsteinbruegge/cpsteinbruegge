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
#import Get_valid_input_New_Amend_Protocol
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
        

    def view_trades(self,row_number=None):
               
        print()
        print(f" In view_trades, Viewing trades in {self.file_name}, row_number: {row_number}")  #debugging line
        print()



        try:
            if not os.path.exists(self.file_name):
                  print("No trade records found.")
                  return
            

            with open(self.file_name , mode='r') as file:  
                print("Debug: File opened successfully - Raw file contents") #debugging line
                print(file.read())
                file.seek(0)

                reader = csv.reader(file)
                data = [row for row in reader if row]  #Skip empty rows
                print(f"Debug: Data read from file: {data}") 
                           
                print(f"Number of rows: {len(data)}")   #debugging line
                if len(data) > 1:
                    headers = data[0] 
                    rows = data[1:]  # Skip the header row; don't prepend row number here
                    
                    if row_number is not None:
                        if 1 <= row_number <= len(rows):
                            print (f"Debug: Row number {row_number} found.")
                            print()
                            #Dynamically add the row number when printing the table

                            rows_with_numbers = [[i + 1] + row for i, row in enumerate(rows)]
                            print(tabulate.tabulate([[rows_with_numbers] + rows[row_number-1]], headers=["Row"]+headers,tablefmt='PIPE'))  
                            return rows  # Return the specific row as a list
                         
                            
                        else:
                            print(f"Row number {row_number} not found.")
                            
                    else:
                        print()  #Print all rows
                        #Dynamically add the row number when printing the table
                        rows_with_numbers = [[i+1] + row for i,row in enumerate(rows)]
                        print(tabulate.tabulate(rows_with_numbers, headers=["Row"]+headers,tablefmt='PIPE')) 

                        #print(tabulate.tabulate(rows, headers=headers, tablefmt='grid'))  # Print the table with grid format
                        #print(tabulate.tabulate(rows, headers=headers, tablefmt='fancy_grid'))  # Print the table with fancy grid format
                        #print(tabulate.tabulate(rows, headers=headers, tablefmt='html'))  # Print the table in HTML format
                        #("Total Rows: ",rows,len(rows))  #debugging line
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
   
            #   # Check if the file exists
    if not os.path.exists(file_name):   
        print(f"File {file_name} does not exist.")
        return  
    # Exit the function if the file does not exist
    # If the file exists, proceed with the Options class            
    Options_Editor = Options(file_name)

    # Initialize Options class with the file name
    Options_Editor.view_trades()  
    print()
    rows = Options_Editor.view_trades()  # Get the current trades from the file     

     # Display the current trades in the file

    #Ask Amend or Delete trade records
   
    # Amend trade records

    if Amend_delete == "A":
        # Ask for the trade row to amend
        trade_row = Get_valid_input.get_valid_int ("Enter the trade row to amend: ")    
        #Display the current trade details
        if 1 <= trade_row <= len(rows): 
           
            #print("Amend Trade, not yet implemented.")              
            print(f"Current trade details: {rows[trade_row-1]}")  #debugging line
            Options_Editor.view_trades(trade_row)  # Display the current trade details
            print()


            
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
            #"Profit/Loss": Get_valid_input.get_valid_float,  # Optional: Recalculate instead of asking

        }

        #Start getting new data and update rows

        # Header row for reference
            headers = ["Symbol", "Date", "C/P", "Strike", "Exp Date", "Premium", "Contracts",
                   "Total Open Premium", "Current Price", "Close Cost", "Status", "Profit/Loss"]

        # Update the row
            updated_row = []
        #debugging line

            #print("Editing trade details:")
            #print(list(enumerate(zip(headers, rows[trade_row-1]), start=1)))  #debugging line
               
        

        #
        # Loop through each field and ask for new values
            print("Press <Space Bar> to enter new value for each field, or press <Enter> to keep current value:")
            print()

            for i, (header, value) in enumerate(zip(headers, rows[trade_row-1][1:])):   # Skip the first column (row number)
                
                    # Edit all other fields
                if not header == "Profit/Loss":  # Skip Profit/Loss field
                    print(f"{header} (Current Value: {value})",end="")  
                    validation_method = field_mapping.get(header)  # Get the corresponding validation method

                    #Check for space bar or enter key

                    if input() ==  " ":

                    
                        if validation_method:
                    # Validate the new value using the corresponding method
                            try:
                                validated_value = validation_method("Amend")
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

                elif header == "Profit/Loss":
                    # Recalculate "Profit/Loss" based on updated values and skip editing this field
                    try:
                        premium = float(updated_row[headers.index("Premium")])  # Adjust index for skipped row number
                        contracts = int(updated_row[headers.index("Contracts")])
                        close_cost = int(updated_row[headers.index("Close Cost")])
                        # Calculate total open premium and profit/loss
                        total_open_premium = premium * contracts * 100
                        profit_loss = int(total_open_premium - close_cost)
                        updated_row.append(f"{profit_loss:.2f}")  # Append recalculated "Profit/Loss"
                        print(f"Recalculated Profit/Loss: {profit_loss}")  # Debugging line
                    except Exception as e:
                        print(f"Error recalculating Profit/Loss: {e}")
                        updated_row.append("Error")  # Append a placeholder in case of error

           # Update the row in the list
                rows[trade_row - 1] = updated_row
                print(f"Updated trade details: {rows[trade_row - 1]}",end="")  #debugging line
                Options_Editor.view_trades(trade_row-1)  
                print()
                # Display the updated trade details
            

        # Save the updated rows back to the file
            try:
                with open(file_name, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)  # Write the header row
                    writer.writerows(rows)  # Write all rows
                    print("File updated successfully.")
                   

            except Exception as e:
                print(f"Error updating file: {e}")
                sys.exit(1)

            Options_Editor.view_trades()  # Display the updated trades after amendment

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
