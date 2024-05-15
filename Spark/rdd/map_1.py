#1-20 element
from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.parallelize([i for i in range(1,21)])
rdd.foreach(print)

#square

print("*"*100)

rdd1=rdd.map(lambda x:(x,x**2)) #pair rdd
rdd1.foreach(print)