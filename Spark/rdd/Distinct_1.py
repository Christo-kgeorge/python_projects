from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/Downloads/sample(1).txt')
rdd.foreach(print)
print("*"*100)

rdd1=rdd.distinct()
rdd1.foreach(print)