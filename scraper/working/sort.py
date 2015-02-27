"""This sorts data based on lat and long."""

from operator import itemgetter
# import dateutil.parser
import csv

with open('mapped.csv', 'r') as csvinput:
    temp_list = csv.reader(csvinput)

    data_sorted = sorted(temp_list, key=itemgetter(6))


with open('mapped_sort.csv', 'wb') as output:
    # output.write(firstline)
    csvwriter = csv.writer(output)
    csvwriter.writerows(data_sorted)
