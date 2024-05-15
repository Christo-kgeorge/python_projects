# Countbyvalue and countbykey

from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/PycharmProjects/Spark/sample')
rdd.foreach(print)

print("*"*100)

rdd1=rdd.flatMap(lambda x:x.split(' '))
rdd1.foreach(print)

print("*"*100)

lst=rdd1.countByValue()
print(lst)

print("*"*100)

# countbykey
#pair rdd ====>count countbykey
rdd2=rdd1.map(lambda x:(x,1))

lst=rdd2.countByKey()
print(lst)