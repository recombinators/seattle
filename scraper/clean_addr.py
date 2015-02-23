"""Code for removing duplicate rows.
Input 1042196 rows
Output 1032442 rows
"""
import csv
from string import replace

with open('clean.csv', 'r') as csvinput:
    temp_list = csv.reader(csvinput)

    new_list = []
    for line in temp_list:
        try:
            if "/" in line[3]:
                line[3] = replace(line[3], '/', 'and')
            new_list.append(line)
        except IndexError:
            continue


with open('clean_addr.csv', 'wb') as output:
    csvwriter = csv.writer(output)
    csvwriter.writerows(new_list)
    # output.write(firstline)
    
    # # import pdb; pdb.set_trace()
    
        
    
    # output.writelines(new_list)
