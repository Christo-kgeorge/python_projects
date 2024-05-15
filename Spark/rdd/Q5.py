from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/Downloads/movies_cleaned_pandas.csv')
rdd.foreach(print)

print("*"*100)

# Q1
row=rdd.count()
print(row)

# Q2
rdd2=rdd.map(lambda x:x.split(','))
rdd1=rdd.distinct()
row1=rdd1.count()
print(row1)

print("*"*100)

# Q3
#rdd2=rdd.map(lambda x:x.split(','))
rdd3=rdd2.sortBy(lambda x:x[2],ascending=False)
rdd3.foreach(print)
print("*"*100)

# Q4
rdd4=rdd2.sortBy(lambda x:x[3],ascending=False).map(lambda x:x[1:-1])
lst=rdd4.take(5)
print(lst)
print("*"*100)

# Q5
rdd4=rdd2.sortBy(lambda x:x[3]).map(lambda x:x[1:-1])
lst=rdd4.take(3)
print(lst)
print("*"*100)

# Q6

rdd5=rdd2.map(lambda x:(x[2],1))
lst=rdd5.countByKey()
print(lst)



