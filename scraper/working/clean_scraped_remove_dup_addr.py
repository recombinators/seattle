"""Code for removing duplicate rows.
Input 1042196 rows
Output 1032442 rows
"""

with open('clean_addr_socrata.csv', 'r') as csvinput:
    temp_list = csv.reader(csvinput)

print 'length pre set: {}'.format(len(temp_list))

set_list = set(temp_list)
print 'length post-set: {}'.format(len(set_list))

with open('clean_socrata.csv', 'wb') as output:
    output.write(firstline)
    output.writelines(set_list)
