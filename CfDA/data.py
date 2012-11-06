import csv

COLS = (2, 7, 11, 17, 23)

for i, line in enumerate(csv.reader(open("outcome-of-care-measures.csv"))):
    print '|'.join([str(i+1)] + [ line[col-1] for col in COLS ])
