import re


def get_valid_ticker_symbol(prompt):

    while True:
        
        
        symbol = input(prompt).strip()  # Remove leading/trailing whitespace
        
        print(f"Debug: User entered {symbol}") #debug

        if re.match(r'^[A-Za-z]{1,4}$', symbol):
            break
        else:
          print("Invalid symbol. Please enter 1-4 letters.")
    return symbol.upper()  # Convert to uppercase for consistency
