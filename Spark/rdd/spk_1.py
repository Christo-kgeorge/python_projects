from pyspark import SparkContext
sc=SparkContext(master='local',appName='jan').getOrCreate()
rdd=sc.parallelize([1,2,3,4])
rdd.foreach(print)