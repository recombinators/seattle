from operator import itemgetter
import pprint
import dateutil.parser
import datetime

# units,date,type,location,incident_number,latitude,longitude


class PST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-8)

    def dst(self, dt):
        return datetime.timedelta(0)


with open('scraped_geocoded.csv', 'r') as csvinput:
    firstline = csvinput.readline()
    temp_list = csvinput.readlines()

    data_list_of_lists = []
    data_bad = []
    for line in temp_list:
        line_split = line.split(',')

        try:
            DEFAULT = datetime.datetime(1900, 01, 01, 00, 00, tzinfo=PST())
            line_split[1] = dateutil.parser.parse(line_split[1], default=DEFAULT).isoformat()
        except ValueError:
            pass

        data_list_of_lists.append(line_split)

    data_sorted = sorted(data_list_of_lists, key=itemgetter(1))
    for i, line in enumerate(data_sorted):
        print(data_sorted[i])
        data_sorted[i] = ','.join(line)


with open('clean_date2.csv', 'wb') as output:
    output.writelines(data_sorted)
