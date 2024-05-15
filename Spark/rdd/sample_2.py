from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/Downloads/sample4.txt')
rdd.foreach(print)

#loc= chennai data collect

print("*"*100)

rdd1=rdd.map(lambda x:x.split(','))
rdd1.foreach(print)

print("*"*100)

rdd2=rdd1.filter(lambda x:x[5]=='Chennai') \
    .map(lambda x:x[1:5])
rdd2.foreach(print)
print("*"*100)

#age above 23 and loc chennai fname lname age

rdd3=rdd1.filter(lambda x:x[3]>'23' and x[5]=='Chennai') \
    .map(lambda x:x[1:4])
rdd3.foreach(print)

