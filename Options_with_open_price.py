import math
import json
import csv
import os
import datetime
import sys

    # Check Git functions
    
    

    # Debugging lines to check current working directory and sys.path
    #print(f"Current working directory: {os.getcwd()}")  #debugging line
    #print(f"Python module search path: {sys.path}")  #debugging line
    #print("\n".join(sys.path))  #debugging line


import tabulate
import Get_valid_input
from Get_valid_input import RestartProgram
import re

#Allow escape from any input in program

def safe_input(prompt):
    while True:
        value= input(prompt).strip()
        if value.lower() == 'x' or value.upper() == 'X':
            print("\n")
            print("Returning to Main Menu")
            print("\n")
            raise RestartProgram
       
        return value
    
#Clean Options.csv file 

with open("Options.csv", newline="") as infile, open("Options_cleaned.csv", "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    header = next(reader)
    writer.writerow(header)
    for row in reader:
        # Pad or trim row to match header length
        if len(row) < len(header):
            row += [""] * (len(header) - len(row))
        elif len(row) > len(header):
            row = row[:len(header)]
        writer.writerow(row)

# Rename the cleaned file to overwrite the original
os.replace("Options_cleaned.csv", "Options.csv")

#Now start the main program

CSV_HEADERS = ["Symbol", "Open Date", "C/P", "Strike", "Exp Date", "Premium", "Contracts", "Total Open Premium", "Current Price", "Open Price", "Close Cost", "Status", "Profit/Loss"]

last_exp_date = None
class Options:
    def __init__(self,file_name):
        self.file_name = file_name

        try:
            if not os.path.exists(self.file_name):
                with open(self.file_name, 'w', newline="") as file:
                  writer = csv.writer(file)
                  writer.writerow(CSV_HEADERS)  # Write the header row
                  
            # ["Symbol" ,"Open Date","C/P","Strike","Exp Date","Premium","Contracts", "Total Open Premium","Current Price","Close Cost", "Status", "Profit/Loss"])
            #debugging line
                
           # with open(self.file_name, 'r', newline="") as file:
           #   reader = csv.reader(file)
           #   data = [row for row in reader if row]
           #   if data:
           #       print("Header row: ",data[0])  
           #   print("All rows: ",data)   #debugging line

        except Exception as e:
            print(f"Error initializing CSV file: {e}")
            sys.exit(1)

   


    def choose_option(self):
        #debug 
        #print("Made it to Options Tracker\n")
        while True:

            print("\nOptions Tracker\n")

            print("1. Enter new trade")
            print("2. View all trades")
            print("3. View trades by month and year of expiration")
            print("4. View trades by year of expiration only")
            print("5. Amend trade records")
            print("6. Delete trade records")
            print("7. Exit Program - or press 'X' at any time to return to Main Menu.")
            print("\n")
         
            choice = safe_input("Enter choice: ").strip()

            print("\n")
         
            if choice == "1":
                self.enter_data()
            elif choice == "2":
                print
                self.view_trades()
            elif choice == "3":
                # View trades by month of expiration
                self.view_trades_by_expiration_month()

            elif choice == "4":
                self.view_trades_by_expiration_year()

            elif choice == "5":
                # Amend or delete trade records
                
                Amend_delete = "A" #Amend trade records
                Options_Trade_Editor(self.file_name, Amend_delete)  
                # os.remove(self.file_name) 
            elif choice == "6":
                Amend_delete = "D" #Delete trade records
                Options_Trade_Editor(self.file_name, Amend_delete) #Delete trade records  
                # os.remove(self.file_name) 
            elif choice == "7":
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

 
    

    def enter_data(self):  
        global last_exp_date     
        
        proceed = True                                  
                
        while proceed:
            #debug
            #print("Made it to enter_data") #debug

            #symbol =self.get_valid_symbol("Enter Symbol: ") 
            #debug    
            #tradedate = Get_valid_input.get_valid_date("Open Date (MM-DD-YYYY); <Enter> for today's date:")    
            
           
            # Create a dictonary data object for the trade record
           
            #debug
            #print(f"Debug: User entered {symbol}") #debug
            tradedate = Get_valid_input.get_valid_date("Open Date (MM-DD-YYYY); <Enter> for today's date: ")
            symbol = Get_valid_input.get_valid_symbol("Enter Symbol: ")
            strike = Get_valid_input.get_valid_int("Enter Strike: ")
            exp_date = Get_valid_input.get_valid_exp_date("Expiration Date (MM-DD-YYYY); <Enter> for last used: ", default_date=last_exp_date)
            last_exp_date = exp_date
            premium = Get_valid_input.get_valid_float("Enter Premium ($x.xx): ", 2)
            contracts = Get_valid_input.get_valid_int("Enter Contracts: ")
            current_price = Get_valid_input.get_valid_int("Enter Current Price: ")

            # Prompt for an open price (optional); if left blank, use current price
            while True:
                open_price_raw = safe_input("Enter Open Price [press Enter to use Current Price]: ")
                if open_price_raw == "":
                    open_price = int(current_price)
                    break
                try:
                    open_price = int(float(open_price_raw))
                    break
                except ValueError:
                    print("Invalid price. Enter numeric value or press Enter to use Current Price.")

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
                "open_price": open_price,
                "close_cost": close_cost,
                "status": status,
                "cp": cp
            }

            # Log the trade (open_price included)
            self.log_trade(
                trade_record["symbol"],
                trade_record["tradedate"],
                trade_record["cp"],
                trade_record["strike"],
                trade_record["exp_date"],
                trade_record["premium"],
                trade_record["contracts"],
                trade_record["current_price"],
                trade_record["open_price"],
                trade_record["close_cost"],
                trade_record["status"]
            )
            last_exp_date = trade_record["exp_date"]  # Update last expiration date

             
            #self.log_trade(symbol,tradedate, cp, strike, exp_date, premium, contracts, current_price, close_cost, status)
            
            #Ask user if they want to add another trade

            while True:   
               answer = safe_input("Add another trade? Y/N ").upper()   
               if answer in {'Y','N'}:
                   break
               else:
                   print("Invalid input. Please enter Y or N.")

            if answer == "N":
                    proceed = False  
                    self.view_trades()  # Display the updated trades after amendment



            elif answer == "Y":
                 proceed = True           
              
    def log_trade (self, symbol, tradedate, cp, strike, exp_date, premium, contracts, current_price, open_price, close_cost, status):
        try:
            #print(f"Debug: premium={premium}, contracts={contracts}, close_cost={close_cost}")  #debugging line
            total_open_premium= int(float(premium) * int(contracts) * 100)
            #print(f"Debug: total_open_premium={total_open_premium}")  #debugging line
            profit_loss = int(total_open_premium - int(close_cost))
            with open(self.file_name, mode='a',newline= "") as file:
                writer = csv.writer(file)
                writer.writerow([
                    symbol,
                    tradedate,
                    cp, 
                    strike,
                    exp_date,
                    f"{float(premium):.2f}",
                    contracts, 
                    total_open_premium,
                    int(current_price),
                    int(open_price),
                    close_cost,


                    status, 
                    int(profit_loss)])
        except Exception as e:
            print(f"Error logging trade: {e}")
            sys.exit(1)
        

    def view_trades(self):
               
        print("\n")

        try:
            if not os.path.exists(self.file_name):
                  print("No trade records found.")
                  return
            

            with open(self.file_name , mode='r') as file:  
                #print("Debug: File opened successfully - Raw file contents") #debugging line
                #print(file.read())
                #file.seek(0)

                reader = csv.reader(file)
                data = [row for row in reader if row]  #Skip empty rows
                #print(f"Debug: Data read from file: {data}") 
               
               
                #print(f"Number of rows: {len(data)}")   #debugging line
                if len(data) > 1:
                    headers =  data[0] 
                    total_open_premium_index = headers.index("Total Open Premium")  # Get the index of the Total Open Premium column
                    close_cost_index = headers.index("Close Cost")  # Get the index of the Close Cost column
                    profit_loss_index = headers.index("Profit/Loss")  # Get the index of the Profit/Loss column 
                    
                     #Sort in alphabetical order by Symbol column (index 1)
                    
                    
                    symbol_index = headers.index("Symbol")  # Get the index of the Symbol column
                    sorted_rows = sorted(data[1:], key=lambda x: x[symbol_index])  # Sort rows by Symbol column
                    rows = []

                    total_open_premium = 0
                    total_close_cost = 0
                    total_profit_loss = 0   

                    # Format Premium column to two decimal places
                    for i, row in enumerate(sorted_rows, start=1):
                     if row:
                         try:
                            row[total_open_premium_index] = f"{int(row[total_open_premium_index])}" 
                         except Exception:
                             pass  # Leave as is if conversion fails
                         try:
                            total_open_premium += int(row[total_open_premium_index])
                         except Exception:
                            pass
                         try:
                            total_close_cost += int(row[close_cost_index])
                         except Exception:
                            pass
                         try:
                            total_profit_loss += int(row[profit_loss_index])
                         except Exception:
                            pass 
                         rows.append([i] + row)
                   
                   
                # Prepare the totals row, aligning with the correct columns
                    totals_row = [''] * (len(headers) + 1)  # +1 for the Row number column
                    totals_row[total_open_premium_index + 1] = f"{total_open_premium}"
                    totals_row[close_cost_index + 1] = f"{total_close_cost}"
                    totals_row[profit_loss_index + 1] = f"{total_profit_loss}"
                    totals_row[0] = "TOTALS"

                    rows.append([''] * len(totals_row))       #Blank line
                    rows.append(totals_row)
                    # Now print the table with row numbers

                    #rows = [[i] + row for i,row in enumerate(data[1:], start=1) if row] 
                    print("\n")
                    headers_with_row = ["Row"] + headers  # Add "Row" header
                    print("\n")
               
                    print(tabulate.tabulate(rows, headers=headers_with_row,tablefmt='PIPE'))   
                    print("\n")
                    print("\n")
                    #print(f"Total Trades: {len(rows)}")  #debugging line
                    
               #debugging line
               #print("Total Rows: ",rows,len(rows))  #debugging line
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
                        print(f"Row {row[0]} Profit/Loss: {row[-1]}")  #debugging line
                        print(f"Debug: Total Profit/Loss so far: {total_profit_loss}")  #debugging line
                    #except ValueError as e:
                    except (ValueError, IndexError):
                        print(f"Error calculating profit/loss for row {row}; skipping.")
                        #debug
                        #print("Row", row)
            print(f"Total Profit/Loss: {total_profit_loss}")
        except Exception as e:
            print(f"Error calculating profit/loss: {e}")
            sys.exit(1)

    def view_trades_by_expiration_month(self):


     print("\n")
     try:
        if not os.path.exists(self.file_name):
            print("No trade records found.")
            
            return

        # Validate month input
        while True:
            month = safe_input("Enter month of expiration (MM): ").zfill(2)
            if re.fullmatch(r"0[1-9]|1[0-2]", month):
                break
            else:
                print("Invalid month. Please enter a value from 01 to 12.")

        # Validate year input
        while True:
            year = safe_input("Enter year of expiration (YYYY): ")
            if re.fullmatch(r"\d{4}", year):
                break
            else:
                print("Invalid year. Please enter a 4-digit year (e.g., 2024).")

        with open(self.file_name , mode='r') as file:
              reader = csv.reader(file)
              data = [row for row in reader if row]
              if len(data) > 1:
                headers = data[0]
                exp_date_index = headers.index("Exp Date")
                total_open_premium_index = headers.index("Total Open Premium")
                close_cost_index = headers.index("Close Cost")
                profit_loss_index = headers.index("Profit/Loss")
                filtered_data = []

                #Initialize totals
                total_profit_loss = 0
                total_open_premium = 0
                total_profit_loss = 0
                total_close_cost = 0


                for row in data[1:]:
                    if row:
                        date_str = row[exp_date_index]

                        #print(f"Debug: Row {i} Exp Date: {date_str}")  #debugging line

                        date_str = date_str.strip()  # Remove any leading/trailing whitespace

                        if "-" in date_str:
                            parts = date_str.split("-")
                        else:
                            parts = date_str.split("/")
                        if len(parts) == 3 and parts[0].zfill(2) == month and parts[2] == year:
                           
                           #Sum totals
                           try:
                             total_open_premium += int(row[total_open_premium_index])
                           except Exception:
                                pass
                           try:
                               total_profit_loss += int(row[profit_loss_index])
                           except Exception:
                               pass
                           try:
                               total_close_cost += int(row[close_cost_index])
                           except Exception:
                               pass

                           filtered_data.append(row)
                           headers_with_row = ["Row"] + headers
                if filtered_data == []:
                   print("\n")
                   print("No trade records found.")
                else:
                   
                    #Sort in alphabetical order by Symbol column (index 1)
                             
                   symbol_index = headers.index("Symbol")  # Get the index of the Symbol column
                   filtered_data = sorted(filtered_data, key=lambda x: x[symbol_index])  # Sort rows by Symbol column
                   filtered_rows = [[i+1] + row for i, row in enumerate(filtered_data)]
                   headers_with_row = ["Row"] + headers
                   print("\n")
                   totals_row = [''] * (len(headers) + 1)
                   totals_row[total_open_premium_index + 1] = f"{total_open_premium}"
                   totals_row[close_cost_index + 1] = f"{total_close_cost}"
                   totals_row[profit_loss_index + 1] = f"{total_profit_loss}"
                   totals_row[0] = "TOTALS"
                   filtered_rows.append([''] * len(totals_row))  # Blank line
                   filtered_rows.append(totals_row)
                   print("\n")
                   print(tabulate.tabulate(filtered_rows, headers=headers_with_row, tablefmt='PIPE'))
                   print("\n")
     except RestartProgram:
         raise RestartProgram
     except Exception as e:
         print(f"Error viewing trades: {e}")
         sys.exit(1)       

   
    
    def view_trades_by_expiration_year(self):


     print("\n")
     try:
        if not os.path.exists(self.file_name):
            print("No trade records found.")
            return

        

        # Validate year input
        while True:
            year = safe_input("Enter year of expiration (YYYY): ")
            if re.fullmatch(r"\d{4}", year):
                break
            else:
                print("Invalid year. Please enter a 4-digit year (e.g., 2024).")

        with open(self.file_name , mode='r') as file:
              reader = csv.reader(file)
              data = [row for row in reader if row]
              if len(data) > 1:
                headers = data[0]
            #Sort in alphabetical order by Symbol column (index 1)                                                          
                symbol_index = headers.index("Symbol")  # Get the index of the Symbol column
                sorted_rows = sorted(data[1:], key=lambda x: x[symbol_index])  # Sort rows by Symbol column
                
                exp_date_index = headers.index("Exp Date")
                total_open_premium_index = headers.index("Total Open Premium")
                close_cost_index = headers.index("Close Cost")
                profit_loss_index = headers.index("Profit/Loss")
                filtered_rows = []

                #Initialize totals
                total_profit_loss = 0
                total_open_premium = 0
                total_profit_loss = 0
                total_close_cost = 0


                for i, row in enumerate(sorted_rows, start=1):
                    if row:
                        date_str = row[exp_date_index]

                        #print(f"Debug: Row {i} Exp Date: {date_str}")  #debugging line

                        date_str = date_str.strip()  # Remove any leading/trailing whitespace

                        if "-" in date_str:
                            parts = date_str.split("-")
                        else:
                            parts = date_str.split("/")
                        if len(parts) == 3 and parts[2] == year:
                           
                           #Sum totals
                           try:
                             total_open_premium += int(row[total_open_premium_index])
                           except Exception:
                                pass
                           try:
                               total_profit_loss += int(row[profit_loss_index])
                           except Exception:
                               pass
                           try:
                               total_close_cost += int(row[close_cost_index])
                           except Exception:
                               pass

                           filtered_rows.append(row)
                           headers_with_row = ["Row"] + headers
                if filtered_rows == []:
                   print("\n")
                   print("No trade records found.")
                else:
                   filtered_rows = sorted(filtered_rows, key=lambda x: x[symbol_index])  # Sort rows by Symbol column
                   filtered_rows = [[i+1] + row for i, row in enumerate(filtered_rows)]
                   print("\n")
                   totals_row = [''] * (len(headers) + 1)
                   totals_row[total_open_premium_index + 1] = f"{total_open_premium}"
                   totals_row[close_cost_index + 1] = f"{total_close_cost}"
                   totals_row[profit_loss_index + 1] = f"{total_profit_loss}"
                   totals_row[0] = "TOTALS"
                   filtered_rows.append([''] * len(totals_row))  # Blank line
                   filtered_rows.append(totals_row)
                   print("\n")
                   
                   headers_with_row = ["Row"] + headers
                   print(tabulate.tabulate(filtered_rows, headers=headers_with_row, tablefmt='PIPE'))
                   print("\n")
     except RestartProgram:
         raise
     
     except Exception as e:
         print(f"Error viewing trades: {e}")
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
    with open(file_name, newline="") as file:
      reader = csv.reader(file)
      data = [row for row in reader if row]
      headers = data[0]
      rows = data[1:]
      symbol_index = headers.index("Symbol")  # Get the index of the Symbol column
      rows = sorted(rows, key=lambda x: x[symbol_index])  # Sort rows by Symbol column
   
    # This line is being changed to above pure data method   #rows = Options_Editor.view_trades()  # Get the current trades from the file     

     # Display the current trades in the file

    #Ask Amend or Delete trade records
   
    # Amend trade records

    if Amend_delete == "A":
        # Ask for the trade row to amend
        trade_row = Get_valid_input.get_valid_int ("Enter the trade row to amend: ")    
        #Display the current trade details
        if 1 <= trade_row <= len(rows): 
            print()

                        
           # print(f"Current trade details: {rows[trade_row-1]}")

            
            #Make sure inputs are valid

            field_mapping = {
            "Symbol": Get_valid_input.validate_symbol,
            "Open Date": Get_valid_input.get_valid_date,
            "C/P": Get_valid_input.get_valid_call_put,
            "Strike": Get_valid_input.get_valid_int,
            "Exp Date": Get_valid_input.get_valid_exp_date,
            "Premium": Get_valid_input.get_valid_float,
            "Contracts": Get_valid_input.get_valid_int,
           #"Total Open Premium": Get_valid_input.get_valid_float,  # Optional: Recalculate instead of asking
            "Current Price": Get_valid_input.get_valid_int,
            "Close Cost": Get_valid_input.get_valid_int,
            "Status": Get_valid_input.get_valid_status,
            #"Profit/Loss": Get_valid_input.get_valid_float,  # Optional: Recalculate instead of asking

        }

        #Start getting new data and update rows

        # Header row for reference
            headers = CSV_HEADERS  # Use the predefined CSV headers
            #["Symbol", "Open Date", "C/P", "Strike", "Exp Date", "Premium", "Contracts","Total Open Premium", "Current Price", "Close Cost", "Status", "Profit/Loss"]

        # Update the row
            updated_row = []
        #debugging line

            #print("Editing trade details:")
            #print(list(enumerate(zip(headers, rows[trade_row-1]), start=1)))  #debugging line


        

        #
        # Loop through each field and ask for new values

            for header, value in zip(headers, rows[trade_row-1]):   # Skip the first column (row number)
                
                    # Edit all other fields
                if not ((header == "Profit/Loss") or (header == "Total Open Premium")):  # Skip Profit/Loss and Total Open Preimum fields
                    print(f"Editing Field: {header} (Current Value: {value})")
                    validation_method = field_mapping.get(header)  # Get the corresponding validation method
                    if validation_method:
                        new_value = safe_input(f"Enter new value for {header} (or press Enter to keep '{value}'): ").strip()
                        if new_value:
                            if new_value.upper() == 'X' or new_value.lower() == 'x':
                                print("Returning to Main Menu")
                                raise RestartProgram


                            try:
                                if validation_method == Get_valid_input.get_valid_float:
                                    validated_value = Get_valid_input.validate_float(new_value, 2)  # Validate the new value
                                elif validation_method == Get_valid_input.get_valid_int:
                                    validated_value = Get_valid_input.validate_int(new_value)  # Validate the new value
                                elif validation_method == Get_valid_input.get_valid_exp_date:
                                    validated_value = Get_valid_input.validate_date(new_value)  # Validate the new value
                                elif validation_method == Get_valid_input.get_valid_date:
                                    validated_value = Get_valid_input.validate_date(new_value)  # Validate the new value
                                else:
                                    validated_value = validation_method(new_value)  # Validate the new value
                                if header == "Premium":    # Always format with two decimal places
                                    updated_row.append(f"{float(validated_value):.2f}")
                                else: 
                                   updated_row.append(validated_value)
                                #print(f"Debug - Updated {header} to {validated_value}")  #debugging line
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
                       if header == "Premium":  # Always format with two decimal places
                            updated_row.append(f"{float(value):.2f}")
                       else:
                            updated_row.append(value)
                elif header == "Total Open Premium":
                        # Recalculate "Total Open Premium" based on updated values and skip editing this field
                        try:                    
                            premium = float(updated_row[headers.index("Premium")])  # Adjust index for skipped row number       
                            contracts = int(updated_row[headers.index("Contracts")])
                            total_open_premium = premium * contracts * 100
                            updated_row.append(f"{total_open_premium:.0f}")  # Append recalculated "Total Open Premium"
                            print(f"Debug - Recalculating Total Open Premium: {total_open_premium}")  #debugging line   
                        except Exception as e:
                            print(f"Error recalculating Total Open Premium; Entering Zero: {e}")
                            updated_row.append("0")
                elif header == "Profit/Loss":
                    # Recalculate "Profit/Loss" based on updated values and skip editing this field
                    

                        premium = float(updated_row[headers.index("Premium")])  # Adjust index for skipped row number
                        contracts = int(updated_row[headers.index("Contracts")])
                        close_cost = int(updated_row[headers.index("Close Cost")])
                        # Calculate total open premium and profit/loss
                        #print(f"Debug - Recalculating Profit/Loss for trade row {trade_row}:")  #debugging line
                        #print(f"Premium: {premium}, Contracts: {contracts}, Close Cost: {close_cost}")  #debugging line

                        total_open_premium = premium * contracts * 100
                        #print(f"Total Open Premium: {total_open_premium}")  #debugging line
                        #print(f"Close Cost: {close_cost}")  #debugging line
                        try:
                            profit_loss = int(total_open_premium - close_cost)
                            updated_row.append(str(int(profit_loss)))  # Append recalculated "Profit/Loss"
                        
                        except Exception as e:
                            print(f"Error recalculating Profit/Loss; Entering Zero: {e}")
                            updated_row.append("0")  # Append a placeholder in case of error    

           # Update the row in the list
                rows[trade_row - 1] = updated_row
                #print(f"Updated trade details: {rows[trade_row - 1]}",end="")  #debugging line
            

        # Save the updated rows back to the file
            try:
                with open(file_name, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(CSV_HEADERS)  # Write the header row
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
                 writer.writerow(CSV_HEADERS)
                     #["Symbol", "Open Date", "C/P", "Strike", "Exp Date", "Premium", "Contracts", "Total Open Premium", "Current Price", "Close Cost", "Status", "Profit/Loss"])  

                 writer.writerows(rows)  # Write all rows except the header

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
    while True:
        try:
        #debugging line
         #print("Made it to main") #debugging line
         #print(f"Current working directory: {os.getcwd()}")  #debugging line
             file_name = "Options.csv"
    
             OptionsTracker = Options(file_name)
             OptionsTracker.choose_option()
        except RestartProgram:   
            print("Restarting Options Tracker...")
            continue

        except Exception as e:
          print(f"Error in main: {e}")
          print("Restarting Options Tracker...")
          # Handle the RestartProgram exception to restart the program
          

        

   
    



if __name__ == "__main__":
    main()


