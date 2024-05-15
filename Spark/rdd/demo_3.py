#1-30 element

from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.parallelize([i for i in range(1,31)])
rdd.foreach(print)