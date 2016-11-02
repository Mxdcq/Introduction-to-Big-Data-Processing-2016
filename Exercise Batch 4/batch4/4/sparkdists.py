from collections import Counter
from pyspark import SparkConf, SparkContext
import json
import os

conf = SparkConf().setAppName("Sparkdists")
sc = SparkContext(conf=conf)
res = sc.wholeTextFiles("/user/student/americana/") \
        .map(lambda x: [x[0], [len(w) for w in x[1].split()]]) \
        .map(lambda x: [x[0], dict(Counter(x[1]))]).collect()

with open('lendists.json', 'w') as outfile:
    for r in res:
        r[1]['file'] = os.path.basename(r[0])
        print >>outfile, json.dumps(r[1])
