"""Code for geocoding address.
"""
import csv
from string import replace
from geopy.geocoders import Nominatim
geolocator = Nominatim()

with open('clean_addr.csv', 'r') as csvinput:
    temp_list = csv.reader(csvinput)
    temp_list.next()

    new_list = []
    count = 0
    for line in temp_list:
        count += 1
        try:
            location = geolocator.geocode("{}, Seattle, WA".format(line[3]))
            line.append(location.latitude)
            line.append(location.longitude)
            new_list.append(line)
        except IndexError, AttributeError:
            print line
            continue
        if count > 10:
            break


with open('geocode.csv', 'wb') as output:
    csvwriter = csv.writer(output)
    csvwriter.writerows(new_list)

