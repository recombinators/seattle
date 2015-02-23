from operator import itemgetter
import pprint
import dateutil.parser
import datetime

with open('clean_addr.csv', 'r') as csvinput:
    firstline = csvinput.readline()
    temp_list = csvinput.readlines()

    data_list_of_lists = []
    data_bad = []
    for line in temp_list:
        line_split = line.split(',')

        try:
            line_split[1] = datetime.datetime.isoformat(
                dateutil.parser.parse(line_split[1]))
        except ValueError:
            pass

        data_list_of_lists.append(line_split)

    data_sorted = sorted(data_list_of_lists, key=itemgetter(1))
    for i, line in enumerate(data_sorted):
        data_sorted[i] = ','.join(line)


with open('clean_date.csv', 'wb') as output:
    output.write(firstline)
    output.writelines(data_sorted)
