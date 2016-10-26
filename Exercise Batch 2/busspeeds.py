# ming

import io
import json
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
from datetime import datetime, timedelta

bus_data_points = {}
bus_speed = {}
bus_location_time = {}
bus_data_points_speed = []

with open('./busdata.json', 'r') as busdata_json:
    databuf = io.StringIO()  # Initialize an empty StringIO file.
    for line in busdata_json:        # Read one line from the original file.
        databuf.write(line)    # Write the read line into the StringIO file.
        if line == '}\n':      # Did we reach the end of a top-level dictionary?
            databuf.seek(0)    # Set the StringIO to enable reading from its beginning.
            data = json.load(databuf)   # Read the single top-level JSON dictionary.
            databuf.close()             # Discard the current StringIO object.
            databuf = io.StringIO()  # Initialize a new empty StringIO object.
            # Now data can be used as a normal Python dictionary.
            # print(data.keys())  # One example: lists the keys of the data dictionary.
            for i in data['body']:
                if i['monitoredVehicleJourney']['lineRef'] not in bus_data_points:
                    bus_data_points[i['monitoredVehicleJourney']['lineRef']] = [i['recordedAtTime'] + i['monitoredVehicleJourney']['vehicleRef']]
                    bus_speed[i['monitoredVehicleJourney']['lineRef']] = [i['monitoredVehicleJourney']['speed']]
                    bus_location_time[i['monitoredVehicleJourney']['lineRef']] = [(i['recordedAtTime'], i['monitoredVehicleJourney']['vehicleLocation'])]
                if (i['recordedAtTime'] + i['monitoredVehicleJourney']['vehicleRef']) not in bus_data_points[i['monitoredVehicleJourney']['lineRef']]:
                    bus_data_points[i['monitoredVehicleJourney']['lineRef']] += [i['recordedAtTime'] + i['monitoredVehicleJourney']['vehicleRef']]
                    bus_speed[i['monitoredVehicleJourney']['lineRef']] += [i['monitoredVehicleJourney']['speed']]
                    bus_location_time[i['monitoredVehicleJourney']['lineRef']] += [(i['recordedAtTime'], i['monitoredVehicleJourney']['vehicleLocation'])]
    databuf.close()           # Discard the StringIO file also in the end.

def haversine(p1, p2):  # p1, p2 coordinate points of form [latitude, longitude].
    # Convert decimal degrees to radians (also ensures values are floats).
    pr1 = [radians(float(p1[0])), radians(float(p1[1]))]
    pr2 = [radians(float(p2[0])), radians(float(p2[1]))]

    # Haversine formula
    dlat = pr2[0] - pr1[0]   # Difference of latitudes.
    dlon = pr2[1] - pr1[1]   # Difference of longitudes.
    a = sin(dlat/2)**2 + cos(pr1[0]) * cos(pr2[0]) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers.
    return c * r

def location_format_change(line_number, bus_location_time_dict):
    line_location_list = []
    line_time_list = []
    for i in range(len(bus_location_time_dict[line_number])):
        line_location_list += [[bus_location_time_dict[line_number][i][1]['longitude'], bus_location_time_dict[line_number][i][1]['latitude']]]
        line_time_list += [bus_location_time_dict[line_number][i][0]]
    return line_location_list, line_time_list

location = []
time = []
location, time = location_format_change('1', bus_location_time)
# print(location)
# print(time)

location_haversine = []
for i in range(len(location)-1):
    location_haversine.append(haversine(location[i], location[i+1]))
# print(location_haversine)

time_change_format = []
for i in range(len(time)-1):
    time_change_format.append(abs(datetime.strptime(time[i],'%Y-%m-%dT%H:%M:%S.%f+03:00') - datetime.strptime(time[i+1],'%Y-%m-%dT%H:%M:%S.%f+03:00')))
# print(time_change_format)

for i in range(len(location_haversine)):
    if timedelta.total_seconds(time_change_format[i]) == 0.0:
        bus_data_points_speed.append(0.0)
    else:
        bus_data_points_speed.append(location_haversine[i] * 3600.0 / timedelta.total_seconds(time_change_format[i]))

plt.plot(bus_speed['1'])
plt.plot(bus_data_points_speed)
plt.savefig('busspeeds.png')
plt.show()