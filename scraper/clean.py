import csv


with open('scrape_combined.csv', 'r') as csvinput:
    csvreader = csvinput.readline()
    print csvreader

    temp_list = []
    for i in range(100):
        temp = csvinput.readline()

    print temp_list
    print 'length pre set: {}'.format(len(temp_list))

    set_list = set(temp_list)
    # print set_list

    with open('clean.csv', 'wb') as output:
        # csvwriter = csv.writer(csvoutput)
        # # print 'set_list[0]'
        # # print set_list[0]
        output.writelines(set_list)

    print 'length post-set: {}'.format(len(set_list))



    # for i in range(1000):
    #     new_list = temp_list.remove(temp_list[i])
    #     if temp_list[i] in new_list:
    #         temp_list



