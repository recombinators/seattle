"""Apply lat long from socrata data addresses to scraped data.
"""
import csv

with open('clean_addr_socrata.csv', 'r') as csvinput:
    temp_list = csv.reader(csvinput)

    dict_ = {}
    for x in temp_list:
        dict_.setdefault(x[0], [x[3], x[4]])
    print 'length dict: {}'.format(len(dict_))

with open('clean_addr.csv', 'r') as csvinput2:
    new_list = []
    temp_list2 = csv.reader(csvinput2)
    temp_list2.next()
    for line in temp_list2:
        lat = 0
        lon = 0
        if line[3] in dict_:
            lat = dict_[line[3]][0]
            lon = dict_[line[3]][1]
        line.append(lat)
        line.append(lon)
        new_list.append(line)


# set_list = set(output)
# print 'length post-set: {}'.format(len(set_list))

with open('mapped.csv', 'wb') as output:
    csvwriter = csv.writer(output)
    csvwriter.writerows(new_list)
