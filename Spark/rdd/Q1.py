from pyspark import SparkContext
sc=SparkContext(master='local',appName='name').getOrCreate()
rdd=sc.textFile('/home/ckg/PycharmProjects/Spark/sample')
rdd.foreach(print)

print("*"*100)

rdd1=rdd.flatMap(lambda x:x.split(' '))
rdd1.foreach(print)

print("*"*100)

vowels='aeiouAEIOU'
rdd2=rdd1.map(lambda x:(x,[1 if i in vowels else 0 for i in x]))
rdd2.foreach(print)

print("*"*100)
rdd3=rdd1.map(lambda x:(x,sum([1 if i in vowels else 0 for i in x])))
rdd3.foreach(print)

print("*"*100)
rdd4=rdd3.sortBy(lambda x:x[1],ascending=False)
rdd4.foreach(print)

