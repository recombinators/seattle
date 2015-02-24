"""Code for removing duplicate rows.
Input 1042196 rows
Output 1032442 rows
"""
import csv

with open('clean_addr_socrata.csv', 'r') as csvinput:
    temp_list = csv.reader(csvinput)
    output = []
    for x in temp_list:
        output.append(x[3])


print 'length pre set: {}'.format(len(output))

set_list = set(output)
print 'length post-set: {}'.format(len(set_list))

# with open('addr_set.csv', 'wb') as output:
#     csvwriter = csv.writer(output)
#     csvwriter.writerows(set_list)
