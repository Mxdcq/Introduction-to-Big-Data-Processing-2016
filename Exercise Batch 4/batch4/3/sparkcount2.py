from pyspark import SparkConf, SparkContext

stopset = set()
with open('stopwords.txt', 'r') as stopfile:
    for w in stopfile.read().split(','):
        stopset.add(w)
conf = SparkConf().setAppName("Sparkcount2")
sc = SparkContext(conf=conf)
stopbc = sc.broadcast(stopset)
text_file = sc.textFile("/user/student/americana/")
counts = text_file.flatMap(lambda line: line.split(" ")) \
             .filter(lambda w: w not in stopbc.value) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b).sortByKey()
counts.saveAsTextFile("/user/student/test40/4_3")
