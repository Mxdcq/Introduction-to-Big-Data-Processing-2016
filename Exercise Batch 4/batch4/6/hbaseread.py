import time
import datetime
import sys
import os
import happybase

def strTimestamp(t):
    return str(int(time.mktime(datetime.datetime.strptime(t[:16], "%Y-%m-%dT%H:%M").timetuple())))
    
conn = happybase.Connection('trafficdata1')
table = conn.table('Datatest')
busLine = sys.argv[1]
startRow = busLine + '-' + strTimestamp(sys.argv[2])
endRow = busLine + '-' + strTimestamp(sys.argv[3])
speeds = {}
for key, data in table.scan(row_start=startRow, row_stop=endRow):
    veh = data['info:vehicle']
    speed = float(data['info:speed'])
    if veh not in speeds or speeds[veh] < speed:
        speeds[veh] = speed
conn.close()
for veh in sorted(speeds):
   print veh, speeds[veh]
