import csv
import re
the_path = "C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\Web History 20220129075919.csv"


# a='informant'     #String that you want to search
# with open(the_path) as f_obj:
#     reader = csv.reader(f_obj, delimiter=',')
#     for line in reader:      #Iterates through the rows of your csv
#         print(line)          #line here refers to a row in the csv
#         if a in line:      #If the string you want to search is in the row
#             print("String found in first row of csv")
#         break

# import csv
# rows = []
# with open(the_path, 'r') as file:
#     csvreader = csv.reader(file)
#     header = next(csvreader)
#     for row in csvreader:
#         rows.append(row)
# print(header)
# print(rows)

csvfile=open(the_path,'r')
for x in csvfile:
    print(x)
    row = x.split(',')
    print(row)
    print(row[1])
    pattern = 'informant'
    if re.search(pattern,row[1]):
        print('run')
        break
