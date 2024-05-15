from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/PycharmProjects/Spark/sample')
rdd.foreach(print)

print("*"*100)
rdd1=rdd.filter(lambda x:x.startswith('I'))
rdd1.foreach(print)