from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/Downloads/sample4.txt')
rdd.foreach(print)

#age above 23 data collect

print("*"*100)

rdd1=rdd.map(lambda x:x.split(','))
rdd1.foreach(print)

print("*"*100)

rdd2=rdd1.filter(lambda x:x[3]>'23')
rdd2.foreach(print)

print("*"*100)

rdd3=rdd1.filter(lambda x:x[5]=='Chennai')
rdd3.foreach(print)