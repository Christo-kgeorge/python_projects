
from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.parallelize([i for i in range(1,26)])
rdd.foreach(print)

print("*"*100)

rdd1=rdd.filter(lambda x:x%2==1).map(lambda x:(x,x**2))
rdd1.foreach(print)