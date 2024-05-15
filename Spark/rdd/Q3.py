from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/Downloads/customer1.txt')
rdd.foreach(print)

print("*"*100)

rdd1=rdd.map(lambda x:x.split(','))
rdd1.foreach(print)

print("*"*100)

rdd2=rdd1.filter(lambda x:x[-1]=='india').map(lambda x:x[1:-1])
rdd2.foreach(print)

print("*"*100)

rdd3=rdd1.filter(lambda x:x[3]>'60') \
    .map(lambda x:x[1:-2])
rdd3.foreach(print)

print("*"*100)

rdd4=rdd1.filter(lambda x:x[-1]=='india' and x[3]>'40').map(lambda x:x[1:-1])
rdd4.foreach(print)

print("*"*100)

rdd5=rdd1.filter(lambda x:x[-1]=='india' and x[4]=='Dancer').map(lambda x:x[1:-1])
rdd5.foreach(print)

print("*"*100)

rdd6=rdd1.map(lambda x:(x[4],1)).reduceByKey(lambda x,y:x+y)
rdd6.foreach(print)

print("*"*100)
rdd7=rdd1.map(lambda x:(x[-1],1)).reduceByKey(lambda x,y:x+y)
rdd7.foreach(print)

print("*"*100)

# rdd8=rdd1.filter(lambda x:x[-1]=='india').map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y)
# rdd8.foreach(print)