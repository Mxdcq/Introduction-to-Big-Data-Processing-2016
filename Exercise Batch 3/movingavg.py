# ming
# configurations should be one .txt file with indexs and numbers
# and a number for window size(eg. numbers.txt 3)

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import sys

window = int(sys.argv[2])

# non-MapReduce implementation
data = [1,3,5,7,9,2,4,6,8,10]

def m_avg(lst, index, window):
    s = max(0, index-window/2)
    e = min(len(lst), index + window/2)
    total = 0
    for i in range(int(s), int(e)):
        total += lst[i]
    return total/window

def moving_average(data, m):
    result = []
    for i in range(len(data)):
        result.append(m_avg(data,i,m))
    return result

print(moving_average(data, 3))

# MapReduce program
class Movingavg(MRJob):

    SORT_VALUES = True

    OUTPUT_PROTOCOL = JSONValueProtocol

    def m_avg(self, lst, index, window):
        s = max(0, index - window / 2)
        e = min(len(lst), index + window / 2)
        total = 0
        for i in range(int(s), int(e)):
            total += lst[i]
        return total / (e - s)

    def moving_average(self, data, m):
        result = []
        for i in range(len(data)):
            result.append(self.m_avg(data, i, m))
        return result

    def mapper(self, _, line):
        line = line.split()
        yield 1, (line[0], line[1])

    def reducer(self, value, pairs):
        data = []
        for item in pairs:
            data.append(float(item[1]))
            if len(data) <= window:
                sum = 0
                for i in data:
                    sum += i
                sum = sum / window
                yield 1, {item[0]: sum},
            if len(data) == window:
                del(data[0])

if __name__ == '__main__':
    Movingavg.run()