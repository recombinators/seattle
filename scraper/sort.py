from operator import itemgetter
import pprint
import dateutil.parser
import datetime

with open('clean.csv', 'r') as csvinput:
    firstline = csvinput.readline()
    temp_list = csvinput.readlines()

    data_list_of_lists = []
    data_bad = []
    for line in temp_list:
        line_split = line.split(',')
        # pprint.pprint(line_split[1])
        try:
            line_split[1] = datetime.datetime.isoformat(dateutil.parser.parse(line_split[1]))
        except ValueError:
            data_bad.append(line_split)

        # pprint.pprint(line_split[1])
        data_list_of_lists.append(line_split)

    data_sorted = sorted(data_list_of_lists, key=itemgetter(1))

    data_sorted_print = data_sorted[:10]

    pprint.pprint(data_bad)
