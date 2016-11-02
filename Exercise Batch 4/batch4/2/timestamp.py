import time
import datetime
import sys

print time.mktime(datetime.datetime.strptime(sys.argv[1], "%d.%m.%YT%H:%M:%S").timetuple())
