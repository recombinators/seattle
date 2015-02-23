

with open('scrape_combined.csv', 'r') as csvinput:
    firstline = csvinput.readline()
    temp_list = csvinput.readlines()

print 'length pre set: {}'.format(len(temp_list))

set_list = set(temp_list)
print 'length post-set: {}'.format(len(set_list))

with open('clean.csv', 'wb') as output:
    # csvwriter = csv.writer(csvoutput)
    # # print 'set_list[0]'
    # # print set_list[0]
    output.write(firstline)
    output.writelines(set_list)
