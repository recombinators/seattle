"""Add a category column"""

import csv

major_list = ['Fire', 'Crime', 'MVI', 'Other']

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

gas_list = ["Natur Gas Leak Inside Comm", "Natur Gas Leak Inside Res.", "Natur Gas Odor Outside", "Natur Gas Odor Inside Resident", "Natural Gas Leak Major", "Natural Gas Odor", "Natural Gas Leak", "Natur Gas Odor Commercial", "Natur Gas Outside,  Major", "Natur Gas Leak Outside Minor", "Natur Gas Leak Inside Comp", "Unk Odor"]

rescue_list = ["Rescue Salt Water", "Rescue Heavy", "Rescue Ice", "Rescue High Angle", "Rescue Confined Space", "Rescue Water Major", "Rescue Lock In/Out", "Rescue Extrication", "Rescue Rope", "Rescue Automobile", "Rescue Elevator", "Rescue Trench", "Rescue Fresh Water", "Rescue Fresh Water Maj", "Rescue Heavy Major", "Rescue Water", "Rescue Saltwater"]

mutual_aid_list = ["Mutual Aid, Strike Eng.", "Mutual Aid, Adv. Life", "Mutual Aid, Task Force", "Mutual Aid, Medic", "Mutual Aid, Ladder", "Mutual Aid, Tech Res", "Mutual Aid, Marine", "Mutual Aid Basic Life", "Mutual Aid, Marine", "Mutual Aid, Aid", "Mutual Aid, Engine", "Mutual Aid, Aid"]

boat_problems_list = ["Boat Taking Water Minr/Sho", "Boat Taking on Water Major", "Boat Under 50' Unknown Sit", "Boat Under 50' Unknown"]

aid_response_list = ["Aid Response Yellow", "Hang-Up, Aid", "Tunnel Aid", "Aid Response", "Aid Response Freeway", "Aid Service"]

hazmat_spill_list = ["Spill, Non-Hazmat", "Fuel Spill", "Hazmat Unk", "Hazardous Decon", "HAZADV - Hazmat Advised", "AFAH - Auto Alarm Hazmat", "Haz Unk", "Hazardous Mat, Spill-Leak", "HazMat MCI", "Hazardous Material w/Fire", "HazMat Reduced"]

response_level_list = ["1RED 1 Unit", "W1RED - 1  Unit", "AFA4 - Auto Alarm 2 + 1 + 1", "3RED - 1 +1 + 1", "4RED - 2 + 1 + 1"]

assault_list = ["Assault w/Weap 7 per Rule", "Assault w/Weapons, Aid", "Assault w/Weapons 14"]

medic_response_list = ["Medic Response, 7 per Rule", "Single Medic Unit", "Medic Response Freeway", "Medic Response, 6 per Rule", "Multiple Medic Resp 14 Per", "Medic Response", "Tunnel Medic", "Automatic Medical Alarm"]

multiple_casuality_list = ["Multiple Casualty Incident"]

aircraft_list = ["Aircraft Standby", "Aircraft Crash"]

water_job_list = ["Water Job Minor", "Water Job Major"]

carbon_monoxide_list = ["COMED Poss Patient", "Activated CO Detector"]

misc_list = ["MUK9 - FIU CAPTAIN K9", "Drill", "Help the Fire Fighter", "LINK - Link Control Center", "Trans to AMR", "EVENT - Special Event", "Investigate In Service", "Investigate Out Of Service", "RMC Chief", "TEST - MIS TEST", "Advised Incident", "Reduce Resp Opposite Tunnel", "Furnace Problem", "Electrical Problem", "Alarm Bell", "Wires Down"]


with open('dataV2.csv', 'r') as csvinput:
    temp_list = csv.reader(csvinput)
    new_list = []
    for row in temp_list:

        if row[2] in fire_list:
            row.append('Fire') # itemization
            row.append('Fire') # category
        elif row[2] in explosion_list:
            row.append('Other')
            row.append('Explosion')
        elif row[2] in mvi_list:
            row.append('MVI')
            row.append('MVI')
        elif row[2] in infectious_list:
            row.append('Other')
            row.append('Infectious')
        elif row[2] in gas_list:
            row.append('Other')
            row.append('Gas')
        elif row[2] in rescue_list:
            row.append('Other')
            row.append('Rescue')
        elif row[2] in mutual_aid_list:
            row.append('Other')
            row.append('Mutual')
        elif row[2] in boat_problems_list:
            row.append('Other')
            row.append('Boat')
        elif row[2] in aid_response_list:
            row.append('Other')
            row.append('Aid')
        elif row[2] in hazmat_spill_list:
            row.append('Other')
            row.append('HAZMAT')
        elif row[2] in response_level_list:
            row.append('Other')
            row.append('Response')
        elif row[2] in assault_list:
            row.append('Crime')
            row.append('Assault')
        elif row[2] in medic_response_list:
            row.append('Other')
            row.append('Medic')
        elif row[2] in multiple_casuality_list:
            row.append('Other')
            row.append('Multiple_Casualty')
        elif row[2] in aircraft_list:
            row.append('Other')
            row.append('Aircraft')
        elif row[2] in water_job_list:
            row.append('Other')
            row.append('Water')
        elif row[2] in carbon_monoxide_list:
            row.append('Other')
            row.append('Carbon')
        elif row[2] in misc_list:
            row.append('Other')
            row.append('Misc')
        else:
            row.append('Other')
            row.append('Misc')

        new_list.append(row)

with open('datav2_incident_cat.csv', 'wb') as output:
    csvwriter = csv.writer(output)
    csvwriter.writerows(new_list)

