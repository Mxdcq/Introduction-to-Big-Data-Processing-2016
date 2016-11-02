import time
import datetime
import sys
import os
os.environ['JAVA_HOME'] = '/usr/java/latest'
import pydoop.hdfs as hdfs
import happybase

def strTimestamp(t):
    return str(int(time.mktime(datetime.datetime.strptime(t[:23], "%Y-%m-%dT%H:%M:%S.%f").timetuple())))
    
conn = happybase.Connection('trafficdata1')
table = conn.table('Datatest')
with hdfs.open('/user/student/busfiles/busdata.json') as input:
    for line in input:
        data = json.loads(line)
        for trip in data['body']:
            bus = trip['monitoredVehicleJourney']
            timestamp = strTimestamp(trip['recordedAtTime'])
            busLine = bus['vehicleRef']
            veh = bus['vehicleRef']
            lat = bus['vehicleLocation']['latitude']
            lon = bus['vehicleLocation']['longitude']
            speed = bus['speed']
            rowKey = busLine + '-' + timestamp
            print rowKey, veh, lat, lon, speed
            table.put(rowKey, {'info:vehicle': veh, 'info:lat': lat, 'info:lon': lon, 'info:speed': speed})
conn.close()
