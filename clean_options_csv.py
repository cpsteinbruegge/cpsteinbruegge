import csv
import os

with open("Options.csv", newline="") as infile, open("Options_fixed.csv", "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for i, row in enumerate(reader):
        if i == 0:
            writer.writerow(row)
        else:
            try:
                row[-1] = str(int(float(row[-1])))
            except Exception:
                row[-1] = "0"
            writer.writerow(row)

# Rename the cleaned file to overwrite the original
os.replace("Options_fixed.csv", "Options.csv")