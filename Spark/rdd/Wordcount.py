from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/PycharmProjects/Spark/sample')
rdd.foreach(print)


print("*"*100)

rdd1=rdd.flatMap(lambda x:x.split(' ')) \
    .map(lambda x:(x,1))
rdd1.foreach(print)

print("*"*100)

#reducebykey

rdd2=rdd1.reduceByKey(lambda x,y:x+y)
rdd2.foreach(print)

