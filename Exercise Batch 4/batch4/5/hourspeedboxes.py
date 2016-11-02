from pyspark import SparkConf, SparkContext

def createPlot(hourData):
    speeds = {}
    uniqs = set()
    for line in hourData[1]:
        dataRow = line.split(',')
        timeVeh = dataRow[0] + dataRow[2]
        if timeVeh not in uniqs:
            uniqs.add(timeVeh)
            busLine = dataRow[1]
            if busLine not in speeds:
                speeds[busLine] = []
            try:
                speeds[busLine].append(float(dataRow[3]))
            except ValueError:
                pass
    x = []
    labs = []
    for busLine in sorted(speeds):
        labs.append(busLine)
        x.append(speeds[busLine])
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    from pylab import rcParams
    rcParams['figure.figsize'] = 10, 3
    import os
    os.environ['JAVA_HOME'] = '/usr/java/latest'
    import pydoop.hdfs as hdfs
    plt.boxplot(x, labels=labs)
    tmpname = "tmp" + hourData[0] + ".png"
    plt.savefig(tmpname)
    hdfs.put(tmpname, "/user/student/test40/speedbox_" + hourData[0] + ".png")
    os.remove(tmpname)

def lineMapper(line):
    dataRow = line.split(',')
    time = dataRow[0]
    hour = time[11:13]
    busLine = dataRow[1]
    veh = dataRow[9]
    speed = dataRow[14]
    return (hour, time + ',' + busLine + ',' + veh + ',' + speed)

conf = SparkConf().setAppName("Hourspeedboxes")
sc = SparkContext(conf=conf)
res = sc.textFile("/user/student/bus_data") \
        .filter(lambda x: not x.startswith('time')) \
        .map(lineMapper).groupByKey() \
        .foreach(createPlot)
