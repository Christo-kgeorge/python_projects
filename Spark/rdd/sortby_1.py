from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/Downloads/sample4.txt')
rdd.foreach(print)

#loc= chennai data collect

print("*"*100)

rdd1=rdd.map(lambda x:x.split(','))
rdd1.foreach(print)

print("*"*100)

rdd2=rdd1.sortBy(lambda x:x[3],ascending=False)
rdd2.foreach(print)
