from pyspark import SparkContext

def main():

    sc = SparkContext(appName = 'SparkWordCount2')

    with open ('./stopwords.txt', 'r') as stopwords:
        broadcastVar = sc.broadcast(stopwords.read().split(','))

    input_file = sc.textFile('/user/student/americana')
    counts = input_file.flatMap(lambda line: line.split()).filter(lambda x: x not in broadcastVar.value).map(lambda word:(word, 1)).reduceByKey(lambda a, b: a + b)
    counts.saveAsTextFile("/user/student/test07/4_3")

    sc.stop()

if __name__ == '__main__':
    main()