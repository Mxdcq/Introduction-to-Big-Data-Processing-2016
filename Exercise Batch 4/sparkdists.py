from pyspark import SparkContext
from operator import add

def main():

    sc = SparkContext(appName = 'Lendists')

    textfile=sc.wholeTextFiles("/user/student/americana")
    wc=textfile.flatMap(actualWork)
    wc=wc.map(lambda x: (x,1)).reduceByKey(add)
    wc=wc.map(lambda x: (x[0].split(";")[0], x[0].split(";")[1]+': '+str(x[1])))
    wc=wc.groupByKey().mapValues(list)
    with open('lendists.json', 'w') as f:
        f.write(str(wc.collect()))

def actualWork(t):
    content=t[1]
    title=t[0]
    content_list=content.split()
    content_list=map(lambda x: title+';'+str(len(x)),content_list)
    return content_list

if __name__ == '__main__':
    main()
