from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/PycharmProjects/Spark/sample')
rdd.foreach(print)