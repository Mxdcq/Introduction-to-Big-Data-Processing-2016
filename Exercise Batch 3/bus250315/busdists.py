# ming

from mrjob.job import MRJob
from mrjob.step import MRStep
from math import radians, cos, sin, asin, sqrt
from mrjob.protocol import JSONValueProtocol
import os

class Busdists(MRJob):

    SORT_VALUES = True

    OUTPUT_PROTOCOL = JSONValueProtocol

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_statistic,combiner=self.combiner_cal,reducer=self.reducer_result)
        ]

    def haversine(self, p1, p2):  # p1, p2 coordinate points of form [latitude, longitude].
        # Convert decimal degrees to radians (also ensures values are floats).
        pr1 = [radians(float(p1[0])), radians(float(p1[1]))]
        pr2 = [radians(float(p2[0])), radians(float(p2[1]))]

        # Haversine formula
        dlat = pr2[0] - pr1[0]  # Difference of latitudes.
        dlon = pr2[1] - pr1[1]  # Difference of longitudes.
        a = sin(dlat / 2) ** 2 + cos(pr1[0]) * cos(pr2[0]) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers.
        return c * r

    def mapper_get_statistic(self, _, line):
        file_name = os.getenv('mapreduce_map_input_file')
        line = line.split(',')
        # time, lineRef, directionRef, dateFrameRef, longitude, latitude, operatorRef, bearing, delay, vehicleRef, journeyPatternRef, originShortName, destinationShortName, originAimedDepartureTime, speed, timeAPI, timeStorage = line
        # yield file_name, (str(time), str(lineRef), int(directionRef), str(dateFrameRef), float(longitude), float(latitude), str(operatorRef), int(bearing), int(delay), str(vehicleRef), str(journeyPatternRef), int(originShortName), int(destinationShortName), int(originAimedDepartureTime), float(speed), int(timeAPI), int(timeStorage))
        yield file_name, [line[9], line[15], [line[5], line[4]]]

    def combiner_cal(self, file_name, statistics):
        distance = []
        statistics = list(statistics)
        for i in range(len(statistics)-1):
            if statistics[i][0] == statistics[i+1][0]:
                distance.append(self.haversine(statistics[i][2], statistics[i+1][2]))
            if statistics[i][0] != statistics[i+1][0]:
                distance.append(0.0)
        yield (file_name, distance), 1

    def reducer_result(self, file_name, values):
        yield None, {file_name[0]: sum(file_name[1])}

if __name__ == '__main__':
    Busdists.run()