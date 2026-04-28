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
    
# CSV header constant (used throughout the module)
# Added 'Price at Exp' column to record the underlying price at expiration
CSV_HEADERS = [
    "Symbol",
    "Open Date",
    "C/P",
    "Strike",
    "Exp Date",
    "Price at Exp",
    "Premium",
    "Total Open Premium",
    "Contracts",
    "Current Price",
    "Close Cost",
    "Status",
    "Profit/Loss",
]


def clean_options_csv(path="Options.csv"):
    """Normalize `path` CSV rows to match header length. Creates a temporary cleaned file
    and atomically replaces the original. If the file doesn't exist, creates it with
    `CSV_HEADERS` as the header.
    """
    tmp_path = os.path.splitext(path)[0] + "_cleaned.csv"
    try:
        with open(path, newline="") as infile, open(tmp_path, "w", newline="") as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            try:
                # Read existing header (if any) but always write the canonical header
                _existing_header = next(reader)
                header = CSV_HEADERS
            except StopIteration:
                # Empty file: write canonical header and replace
                writer.writerow(CSV_HEADERS)
                os.replace(tmp_path, path)
                return
            writer.writerow(header)
            for row in reader:
                # Pad/truncate rows to match canonical header length
                if len(row) < len(header):
                    row += [""] * (len(header) - len(row))
                elif len(row) > len(header):
                    row = row[:len(header)]
                writer.writerow(row)
        os.replace(tmp_path, path)
    except FileNotFoundError:
        # If the file doesn't exist, create it with the canonical header
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
    except Exception as e:
        print(f"Warning: failed to clean CSV '{path}': {e}")

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
            # Optional Price at Exp (may be unknown at entry time) - store as integer
            price_at_exp_input = safe_input("Enter Price at Exp (integer, optional - press Enter to skip): ")
            if price_at_exp_input == "":
                price_at_exp = ""
            else:
                try:
                    validated = Get_valid_input.validate_int(price_at_exp_input)
                    price_at_exp = str(int(validated))
                except Exception:
                    print("Invalid Price at Exp entered; leaving blank.")
                    price_at_exp = ""
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
                "price_at_exp": price_at_exp,
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
                trade_record["price_at_exp"],
                trade_record["premium"],
                trade_record["contracts"],
                trade_record["current_price"],
                trade_record["close_cost"],
                trade_record["status"],
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
    def log_trade (self,symbol, tradedate, cp, strike, exp_date, price_at_exp, premium, contracts, current_price, close_cost, status):
        try:
            #print(f"Debug: premium={premium}, contracts={contracts}, close_cost={close_cost}")  #debugging line
            total_open_premium= int(float(premium) * int(contracts) * 100)
            #print(f"Debug: total_open_premium={total_open_premium}")  #debugging line
            profit_loss = int(total_open_premium - close_cost)
            with open(self.file_name, mode='a',newline= "") as file:
                writer = csv.writer(file)
                # Ensure Price at Exp is written as integer (or blank)
               

                writer.writerow([
                    symbol,
                    tradedate,
                    cp,
                    strike,
                    exp_date,
                    price_at_exp,
                    f"{float(premium):.2f}",
                    total_open_premium,
                    contracts,
                    int(current_price),
                    close_cost,
                    status,
                    int(profit_loss),
                ])
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
                data = [row for row in reader if row]  # Skip empty rows

            if len(data) == 1:
                print("No trade records found.")
                return

            total_profit_loss = 0
            for row in data[1:]:
                try:
                    total_profit_loss += int(row[-1])
                    print(f"Row {row[0]} Profit/Loss: {row[-1]}")  # debugging line
                    print(f"Debug: Total Profit/Loss so far: {total_profit_loss}")  # debugging line
                except (ValueError, IndexError):
                    print(f"Error calculating profit/loss for row {row}; skipping.")

            print(f"Total Profit/Loss: {total_profit_loss}")
        except Exception as e:
            print(f"Error calculating profit/loss: {e}")
            sys.exit(1)


