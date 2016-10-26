# ming

import io
import json

bus_vehicles = {}
bus_data_points = {}

with open('./busdata.json', 'r') as busdata_json:
    databuf = io.StringIO()  # Initialize an empty StringIO file.
    for line in busdata_json:        # Read one line from the original file.
        # print(line)
        databuf.write(line)    # Write the read line into the StringIO file.
        if line == '}\n':      # Did we reach the end of a top-level dictionary?
            databuf.seek(0)    # Set the StringIO to enable reading from its beginning.
            data = json.load(databuf)   # Read the single top-level JSON dictionary.
            databuf.close()             # Discard the current StringIO object.
            databuf = io.StringIO()  # Initialize a new empty StringIO object.
            # Now data can be used as a normal Python dictionary.
            # print(data.keys())  # One example: lists the keys of the data dictionary.
            # print(data['body'][0].keys())
            for i in data['body']:
                if i['monitoredVehicleJourney']['lineRef'] not in bus_vehicles:
                    bus_vehicles[i['monitoredVehicleJourney']['lineRef']] = [i['monitoredVehicleJourney']['vehicleRef']]
                if i['monitoredVehicleJourney']['vehicleRef'] not in bus_vehicles[i['monitoredVehicleJourney']['lineRef']]:
                    bus_vehicles[i['monitoredVehicleJourney']['lineRef']] += [i['monitoredVehicleJourney']['vehicleRef']]
                if i['monitoredVehicleJourney']['lineRef'] not in bus_data_points:
                    bus_data_points[i['monitoredVehicleJourney']['lineRef']] = [i['recordedAtTime'] + i['monitoredVehicleJourney']['vehicleRef']]
                if (i['recordedAtTime'] + i['monitoredVehicleJourney']['vehicleRef']) not in bus_data_points[i['monitoredVehicleJourney']['lineRef']]:
                    bus_data_points[i['monitoredVehicleJourney']['lineRef']] += [i['recordedAtTime'] + i['monitoredVehicleJourney']['vehicleRef']]
    databuf.close()           # Discard the StringIO file also in the end.

for key in sorted(bus_vehicles.keys()):
    print(str(key) + ": " + str(len(bus_vehicles[key])) + " vehicles and " + str(len(bus_data_points[key])) + " data points")

# print(bus_vehicles)
# print(bus_datapoints)