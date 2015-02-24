"""Split geo coded and non-geocoded data into two separate files."""

import csv

with open('mapped.csv', 'r') as csvinput:
    # firstline = csvinput.readline()
    temp_list = csv.reader(csvinput)
    gc = []
    non_gc = []
    for line in temp_list:

        if line[6] == '0':
            non_gc.append(line)

        else:
            gc.append(line)

with open('mapped_gc.csv', 'wb') as output:
    csvwriter = csv.writer(output)
    csvwriter.writerows(gc)

with open('mapped_non_gc.csv', 'wb') as output:
    csvwriter = csv.writer(output)
    csvwriter.writerows(non_gc)