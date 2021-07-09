import csv
import os

filename = os.path.join(os.getcwd(), 'CSV_Files/institute.csv')

with open(filename, encoding="latin-1") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    l = []

    for row in csv_reader:
        if row[-3] != '':
            l.append(row[-3])
        if row[-2] != '':
            l.append(row[-2])
        if row[-1] != '':
            l.append(row[-1])

    l = set(l)
    l = list(l)
    # print(l)

l = [i.lower() for i in l]

d = {}
d["institutes"] = l

print("dictionary = ", d)
