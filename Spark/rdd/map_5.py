from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/PycharmProjects/Spark/sample')
rdd.foreach(print)

print("*"*100)

rdd1=rdd.map(lambda x:'yes' if 'e' in x else 'no')
rdd1.foreach(print)

print("*"*100)

rdd2=rdd.map(lambda x:x.startswith('I'))
rdd2.foreach(print)
