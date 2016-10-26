#ming

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import OrderedDict
from mrjob.protocol import JSONValueProtocol
import os

class LenDists(MRJob):

    OUTPUT_PROTOCOL = JSONValueProtocol

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(mapper=self.mapper_format, reducer=self.reducer_format)
        ]

    def mapper(self, _, line):
        # file_name = os.environ['map_input_file']
        file_name = os.getenv('mapreduce_map_input_file')
        for word in line.split():
            yield (file_name, len(word)), 1

    def reducer(self, individualWordLength, total):
        yield individualWordLength, sum(total)

    def mapper_format(self, fileLengthPair, totalNum):
        yield fileLengthPair[0], (fileLengthPair[1], totalNum)

    def reducer_format(self, fileName, lengthList):
        json_output = OrderedDict()
        json_output['file'] = fileName
        for item in lengthList:
            json_output[item[0]] = item[1]
        yield None, json_output

if __name__ == '__main__':
    LenDists.run()
