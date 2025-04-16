#Editing data with cursor placement
import curses

def edit_row(stdscr, row):
    curses.echo()
    updated_row = []
    for i, value in enumerate(row):
        stdscr.addstr(0, 0, f"Field {i + 1} ({value}): ")
        stdscr.clrtoeol()
        new_value = stdscr.getstr().decode("utf-8").strip()
        updated_row.append(new_value if new_value else value)
    return updated_row

# Example usage
row = ["AAPL", "04-14-2025", "C", "150", "04-20-2025", "2.50", "10", "2500", "145", "0", "Open", "0"]
updated_row = curses.wrapper(edit_row, row)
print(updated_row)