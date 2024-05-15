from pyspark import SparkContext
sc=SparkContext(master='local',appName='jan').getOrCreate()
rdd=sc.parallelize({2,6,8,3,6,10,11,13})
rdd.foreach(print)