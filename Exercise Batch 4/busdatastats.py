# ming

import io
import json

with open('./busdata.json', 'r') as busdata_json:
    databuf = io.StringIO()  # Initialize an empty StringIO file.
    for line in busdata_json:        # Read one line from the original file.
        # print(line)
        databuf.write(line)    # Write the read line into the StringIO file.
        if line == '}\n':      # Did we reach the end of a top-level dictionary?
            databuf.seek(0)    # Set the StringIO to enable reading from its beginning.
            data = json.load(databuf)   # Read the single top-level JSON dictionary.
            with open('./busdata_single_line.json', 'a') as single_line:
                json.dump(data, single_line)
                single_line.write('\n')
            databuf.close()             # Discard the current StringIO object.
            databuf = io.StringIO()  # Initialize a new empty StringIO object
    databuf.close()           # Discard the StringIO file also in the end.