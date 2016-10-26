import urllib.request
import sys
import time

interval_time = sys.argv[2]
total_time = sys.argv[3]
print(interval_time, total_time)

data = urllib.request.urlopen("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")
page_content = data.read()

start_time = time.time()

with open("./%s" % sys.argv[1], "bw") as f:
    while time.time() - start_time <= float(total_time):
        f.write(page_content)
        time.sleep(int(interval_time))