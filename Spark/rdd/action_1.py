#action:python collection

# collect()
# take()
# first()
# countbykey
# countbyvalue

from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.parallelize([i for i in range(1,26)])

#collect
lst=rdd.collect()
print(lst)

print("*"*100)

# take
# take is similar to limit

lst=rdd.take(5)
print(lst)

print("*"*100)

#first
lst=rdd.first()
print(lst)