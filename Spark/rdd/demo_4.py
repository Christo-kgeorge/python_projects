#1-50 element with incr 2

from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.parallelize([i for i in range(1,51)if i%2==0])
rdd.foreach(print)