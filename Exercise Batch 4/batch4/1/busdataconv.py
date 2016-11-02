import json
from sys import argv
from datetime import datetime
import StringIO

busdata = {}
outfile = open(argv[2], 'w')
with open(argv[1], 'r') as infile:
    databuf = StringIO.StringIO()
    for line in infile:
        databuf.write(line)
        if line == '}\n':
            databuf.seek(0)
            data = json.load(databuf)
            databuf.close()
            databuf = StringIO.StringIO()
            json.dump(data, outfile)
            outfile.write("\n")
    databuf.close()
outfile.close()
