"""Code for removing duplicate rows.
Input 1042196 rows
Output 1032442 rows
"""
import csv
from string import replace

with open('clean_socrata.csv', 'r') as csvinput:
    temp_list = csv.reader(csvinput)

    new_list = []
    for line in temp_list:
        try:
            if "/" in line[0]:
                line[0] = replace(line[0], '/', 'and')
            new_list.append(line)
        except IndexError:
            continue


with open('clean_addr_socrata.csv', 'wb') as output:
    csvwriter = csv.writer(output)
    csvwriter.writerows(new_list)
    # output.write(firstline)
    
    # # import pdb; pdb.set_trace()
    
        
    
    # output.writelines(new_list)
