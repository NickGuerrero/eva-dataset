import re
import random

def eva_format(line):
    # Prepare for write
    stamp = "{ "
    stamp += '"_id": "' + line[0] + '", '
    stamp += '"Country": "' + line[1] + '", '
    # Crew, convert to hybrid array or single value
    stamp += '"Crew": '
    tmp = re.split(" \s+|\t|\n", line[2].strip())
    stamp += '["' + '","'.join(tmp) + '"], ' if len(tmp) >= 2 else '"' + tmp[0] + '", '
    # Vehicle
    stamp += '"Vehicle": "' + re.sub('\s\s+', '', line[3]) + '", ' if line[3] != '' else ''
    # Date, convert to ISODate
    if line[4] != "":
        tmp = line[4].split("/")
        dt_tmp = [tmp[2], tmp[0], tmp[1]]
        stamp += '"Date": {"$date": "' + "-".join(dt_tmp) + 'T00:00:00.00Z" },'
    # Duration, convert to seconds
    if line[5] != "":
        tmp = line[5].split(":")
        secs = int(tmp[0]) * 60 + int(tmp[1])
        stamp += '"Duration": ' + str(secs) + ', '
    # Purpose, convert to array of strings
    stamp += '"Purpose": ['
    # We only want the first 10 or so
    tmp = re.sub('[^a-zA-Z0-9 ]', '', line[6]).strip().lower().split(maxsplit=11)
    if len(tmp) > 10: tmp.pop()
    stamp += '"' + '","'.join(tmp) + '"]' if len(tmp) > 0 else ']'
    return stamp + " }"

# Generate new documents
# Some Country data: https://www.oecd-ilibrary.org/docserver/9789264113565-15-en.pdf?expires=1649572580&id=id&accname=guest&checksum=BDA2ADF870C694080650B4DA22E62BC3
# Grab field names => EVA #,Country,    Crew,Vehicle,Date,Duration,Purpose 
def eva_generate(id_no, countries, crews, vehicles, purposes):
    # Generate a date
    da_num = [random.randint(1, 12), random.randint(1, 30), str(random.randint(1970, 2020))]
    date = str(da_num[0]) + "/" if da_num[0] > 9 else "0" + str(da_num[0]) + "/"
    date += str(da_num[1]) if da_num[1] > 9 else "0" + str(da_num[1])
    date += "/" + str(da_num[2])
    line = [str(id_no), countries[random.randint(0, 6)], crews[random.randint(0, len(crews) - 1)],
        vehicles[random.randint(0, len(vehicles) - 1)], date, str(random.randint(0, 10)) + ":" + str(random.randint(0, 59)),
        purposes[random.randint(0, len(purposes) - 1)]]
    return line


crews = 0 # Create list of prev names and add them here
vehicles = 0 # Create list of prev spacecraft
dates = 0 # Create range, year range from 1970 to 2020


# File locations
eva_csv = open("Extra-vehicular_Activity__EVA__-_US_and_Russia.csv",'r')
eva_json = open("eva.json", "w")
extra_json = open("extra.json", "w")
more_json = open("more.json", "w")
evenmore_json = open("evenmore.json", "w")

# Grab field names => EVA #,Country,Crew,Vehicle,Date,Duration,Purpose 
line = eva_csv.readline().split(",")
fields = ["_id", "Country", "Crew", "Vehicle", "Date", "Duration", "Purpose"]

# Prepare to generate more data
# Grab field names => EVA #,Country, Crew,Vehicle,Date,Duration,Purpose 
id_counter = 0
crews = set()
vehicles = set()
purposes = []

# Pull data from the csv file
while line != ['']:
    id_counter += 1
    line = eva_csv.readline().split(",", maxsplit=6)
    # Check that the line data is valid
    while len(line) != len(fields) and line != ['']:
        print("Error with the line: " + str(id_counter) + " Please re-write the lines with the appropriate NULL values")
        print(line)
        line = input().split(",", maxsplit=6)
    # Add to list reserves
    if line != ['']:
        crews.add(line[2])
        vehicles.add(line[3])
        purposes.append(line[6])
    if line != ['']: eva_json.write(eva_format(line) + "\n")

# Generate more data if necessary
generate_no = 1000
crews = list(crews)
vehicles = list(vehicles)
countries = ["USA", "Russia", "China", "Japan", "India", "Israel", "Iran"]
for i in range(generate_no):
    #id_counter += 1
    extra_json.write(eva_format(eva_generate(id_counter, countries, crews, vehicles, purposes)) + "\n")
    id_counter += 1
    
# Generate a lot more data if necessary
generate_no = 10000
crews = list(crews)
vehicles = list(vehicles)
countries = ["USA", "Russia", "China", "Japan", "India", "Israel", "Iran"]
for i in range(generate_no):
    more_json.write(eva_format(eva_generate(id_counter, countries, crews, vehicles, purposes)) + "\n")
    id_counter += 1
    
# Generate a lot lot more data if necessary
generate_no = 10000
crews = list(crews)
vehicles = list(vehicles)
countries = ["USA", "Russia", "China", "Japan", "India", "Israel", "Iran"]
for i in range(generate_no):
    evenmore_json.write(eva_format(eva_generate(id_counter, countries, crews, vehicles, purposes)) + "\n")
    id_counter += 1

# Close the documents
eva_csv.close()
eva_json.close()
extra_json.close()
more_json.close()
evenmore_json.close()