"""Code for fixing address column. Finds '/' and replaces with 'and'.
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
