from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/PycharmProjects/Spark/sample')
rdd.foreach(print)

print("*"*100)
#newrdd=oldrdd.flatMap(condition)

rdd1=rdd.flatMap(lambda x:x.split(' '))
rdd1.foreach(print)

