from operator import itemgetter
# import dateutil.parser
import csv

with open('mapped.csv', 'r') as csvinput:
    # firstline = csvinput.readline()
    temp_list = csv.reader(csvinput)

    # data_list_of_lists = []
    # data_bad = []
    # for line in temp_list:
    #     line_split = line.split(',')

    #     # try:
    #     #     line_split[1] = datetime.datetime.isoformat(
    #     #         dateutil.parser.parse(line_split[1]))
    #     # except ValueError:
    #     #     pass

    #     data_list_of_lists.append(line_split)

    data_sorted = sorted(temp_list, key=itemgetter(6))
    # for i, line in enumerate(data_sorted):
    #     data_sorted[i] = ','.join(line)


with open('mapped_sort.csv', 'wb') as output:
    # output.write(firstline)
    csvwriter = csv.writer(output)
    csvwriter.writerows(data_sorted)
