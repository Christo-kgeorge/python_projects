from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.parallelize([i for i in range(1,51)])
rdd.foreach(print)

print("*"*100)

rdd1=rdd.map(lambda x:(x,'small') if x<=15 else (x,'medium') if x<=35 else (x,'large'))
rdd1.foreach(print)