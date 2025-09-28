import re


def get_valid_symbol(prompt):
    while True:
            # Get valid input for symbol
        print(f"Debug: In get_valid_symbol") #debug
        symbol = input(prompt)
            #debug
        print(f"Debug: User entered {symbol}") #debug

        if re.match(r'^[A-Za-z]{1,4}$', symbol):
            break
        else:
          print("Invalid symbol. Please enter 1-4 letters.")
    return symbol.upper()  # Convert to uppercase for consistency
            