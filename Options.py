import math
import json
import csv
import os
import sys
import datetime
import tabulate
import Get_valid_input
import re




class Options:
    def __init__(self,file_name):
        self.file_name = file_name

        try:
            if not os.path.exists(self.file_name):
                with open(self.file_name, 'w') as f:
                  writer = csv.writer(f)
                  writer.writerow(["Symbol" ,"Date","C/P","Strike","Exp Date","Premium","Contracts", "Total Open Premium","Current Price","Close Cost", "Status", "Profit/Loss"])
            
        except Exception as e:
            print(f"Error initializing CSV file: {e}")
            sys.exit(1)

    def choose_option(self):
        while True:

            print("\nOptions Tracker")
            print("1. Enter new trade")
            print("2. View trades")
            print("3. Profit/Loss")
            print("4. Exit")
         
            choice = input("Enter choice: ")
         
            if choice == "1":
                self.enter_data()
            elif choice == "2":
                self.view_trades()
            elif choice == "3":
                pass
            elif choice == "4":
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

    def get_valid_date(self, prompt):
        while True:
            date_str = input(prompt)
            try:
                date =  datetime.datetime.strptime(date_str, "%m-%d-%Y")
                return date.date()
            except ValueError:
                print("Invalid date. Please try again.")

    def get_valid_symbol(self, prompt):
        while True:
            symbol = input(prompt)  
            if re.match(r'^[A-Za-z]{1,4}+$', symbol):
                return symbol.upper()
            else:
                print("Invalid symbol. Please enter 1-4 letters.")
            



    def enter_data(self):       
        
        proceed = True                                  
        
        while proceed:

            symbol = self.get_valid_symbol("Enter Symbol: ").upper()    
            #debug    
            tradedate = self.get_valid_date("Enter Date (MM-DD-YYYY):")    
            while True:
                cp = input("Enter C/P: ").upper()
                if cp == "C" or cp == "P":
                    break
                else:
                    print("Invalid input. Please enter C or P.")

            strike = Get_valid_input.get_valid_int("Enter Strike: ")
            exp_date = Get_valid_input.get_valid_date("Enter Exp Date (MM-DD-YYYY): ")
            premium = Get_valid_input.get_valid_float("Enter Premium ($x.xx): ",2)   
            contracts = Get_valid_input.get_valid_int("Enter Contracts: ")
            current_price = Get_valid_input.get_valid_int("Enter Current Price: ")
            close_cost = Get_valid_input.get_valid_int("Enter Close Cost: ")
            #Get status
            while True:

                status = input("Enter Status: O/C: ").upper()
                if status == "O" or status == "C":
                    break   
                else:
                    print("Invalid input. Please enter (O)pen or (C)losed.")
             
            self.log_trade(symbol,tradedate, cp, strike, exp_date, premium, contracts, current_price, close_cost, status)
            
            #Ask user if they want to add another trade

            while True:   
               answer = input("Add another trade? Y/N ").upper()   
               if answer in {'Y','N'}:
                   break
               else:
                   print("Invalid input. Please enter Y or N.")

            if answer == "N":
               proceed = False  
            elif answer == "Y":
               proceed = True           
              
    def log_trade (self,symbol, tradedate, cp, strike, exp_date, premium, contracts, current_price, close_cost, status,):
        try:
            total_open_premium= float(premium) * int(contracts) * 100
            profit_loss = int(total_open_premium - close_cost)
            with open(self.file_name, mode='a') as file:
                writer = csv.writer(file)
                writer.writerow([symbol, tradedate, cp, strike, exp_date, premium, contracts, f"{total_open_premium:.0f}" , int(current_price), close_cost, status, int(profit_loss)])
        except Exception as e:
            print(f"Error logging trade: {e}")
            sys.exit(1)
        

    def view_trades(self):
        try:
            if not os.path.exists(self.file_name):
                  print("No trade records found.")
                  return
            with open(self.file_name , mode='r') as file:
                reader = csv.reader(file)
                data = list(reader)
               # print("DATE READ FROM FILE", data)
            if len(data) > 1:
               headers =  data[0] 
               rows = data[1:]
               print("\n")  
               print(tabulate.tabulate(rows, headers=headers,tablefmt='PIPE'))               
               
            else:
                print("No trade records found.")

        except Exception as e:
            print(f"Error viewing trades: {e}")
            sys.exit(1)   

def main():
    file_name = "Options.csv"
    OptionsTracker = Options(file_name)
    OptionsTracker.choose_option()
    



if __name__ == "__main__":
    main()
