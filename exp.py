import csv

with open('pls.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
    data = filter(None, data)

    for r in data:
        print(r)