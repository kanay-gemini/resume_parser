from pandas import read_csv
import csv

# with open('/home/kanay/projects/CSV_Files/institute.csv', encoding="latin-1") as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter='\t')
#     l = []
#     line_count = 0
 
#     for row in csv_reader:
#         # if line_count < 4:
#         # print(row)
#         # print(row[-2])
#         if row[-3] != '':
#             l.append(row[-3])
#         if row[-2] != '':
#             l.append(row[-2])
        
#         line_count += 1
#     l = set(l)
#     l =list(l)
#     # print(l)
# l = [i.lower() for i in l]
# print("index = ", l.index('no'))
# # print(l)
# d = {}
# d["institutes"] = l

# # print("dictionary = ", d)

with open('/home/kanay/projects/CSV_Files/institute.csv', encoding="latin-1") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    l = []
    line_count = 0
 
    for row in csv_reader:
        # if line_count < 4:
        # print(row)
        # print(row[-2])
        # if row[-3] != '':
        #     l.append(row[-3])
        if row[-2] != '':
            l.append(row[-2])
        
        line_count += 1
    l = set(l)
    l =list(l)
l = [i.lower() for i in l]
# print("index = ", l.index('no'))
d = {}
d["institutes"] = l

print("dictionary = ", d)