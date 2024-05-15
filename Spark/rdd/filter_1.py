#filter


from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.parallelize([i for i in range(1,16)])
rdd.foreach(print)

print("*"*100)
rdd1=rdd.filter(lambda x:x%2==0)
rdd1.foreach(print)