import csv
# with open('eggs.csv', newline='') as csvfile:
with open('../data/van_halen_discography.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        print(', '.join(row))