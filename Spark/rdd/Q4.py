from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/Downloads/sample4.txt')
rdd.foreach(print)

print("*"*100)
rdd1=rdd.map(lambda x:x.split(','))
# rdd1.foreach(print)


rdd2=rdd1.sortBy(lambda x:x[3],ascending=False) \
    .map(lambda x:x[1:-1])
rdd2.foreach(print)

print("*"*100)

lst=rdd2.take(2)
print(lst)

print("*"*100)
#Q2
rdd3=rdd1.sortBy(lambda x:x[3],ascending=True) \
    .map(lambda x:x[1:-1])
rdd3.foreach(print)

print("*"*100)

lst=rdd3.take(1)
print(lst)

#Q3
rdd4=rdd1.filter(lambda x:x[-1]=='Chennai').sortBy(lambda x:x[3],ascending=False).map(lambda x:x[1:-2])
rdd4.foreach(print)

print("*"*100)

lst=rdd4.first()
print(lst)