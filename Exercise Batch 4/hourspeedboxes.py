from pyspark import SparkContext

def main():

    sc = SparkContext(appName = 'hourspeed')

    textfile = sc.textFile("/user/student/bus_data")
    item = textfile.flatMap(lambda line: line.split(','))
    item = item.map(lambda line: ((line[0],line[1]),[line[14]])).reduceByKey(lambda a, b: a + b)
    item = item.groupByKey().mapValues(list)

def your_plotting_function(speed_list):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt




if __name__ == '__main__':
    main()
