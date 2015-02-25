"""Add a category column"""

import csv

with open('dataV2.csv', 'r') as csvinput:
    temp_list = csv.reader(csvinput)

    fire_list = ['Automatic Fire Alarm False', 'Automatic Fire Dist 11',
                 'Automatic Fire Fire Dist 11', 'Brush Fire', 'Car Fire',
                 'Fire in Building', 'Food On The Stove Out', 'Tanker Fire',
                 "Ship Fire 50' on Water", 'Bark Fire', 'Dumpster Fire',
                 'Shed Fire', 'Brush Fire Freeway', 'Food On The Stove',
                 'Illegal Burn', 'Fire House Boat', "Ship Fire 50'on Shore/Pier",
                 'Monorail Fire on the beam',  'Vault Fire (Electrical)',
                 'Dumpster Fire W/Exp.', 'Fire Response Freeway', 'Pier Fire',
                 'Brush Fire W/Exp.', 'Fire in Single Family Res',
                 'Boat Fire In Marina', 'Rubbish Fire', 'Auto Fire Alarm',
                 'Chimney Fire', 'Automatic Fire Alarm Resd', "Boat Under 50'",
                 'Fire Shore', 'Tunnel Fire', 'Tranformer Fire', 'Hang-Up, Fire',
                 'Car Fire Freeway', 'Garage Fire', 'Car Fire W/Exp.',
                 "Boat Under 50'", 'Fire Water']

    explosion_list = ["Explosion Major", "Explosion Unk Situation",
                      "Explosion Minor"]

    mvi_list = ["MVI Freeway", "Motor Vehicle Accident", "MVI Freeway Medic",
                "Motor Vehicle Accident Freeway", "MVI - Motor Vehicle Incident",
                "Motor Vehicle Incident", "MVI Medic",
                "Motor Vehicle Incident Freeway"]

    infectious_list = ["Aid Resp Infectious", "Med 7 Resp Infectious",
                       "Medic Resp Infectious"]


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
