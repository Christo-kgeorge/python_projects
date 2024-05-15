from pyspark.sql import SparkSession
ss=SparkSession.builder.master('local[1]').appName('jan').getOrCreate()

lst=[['101','aswin','h',25,'bigdata',3500],
     ['102','gautham','h',28,'python',5000],
     ['103','amith','p',22,'testing',6500],
     ['104','alan','c',21,'python',5500],
     ['105','jovel','j',24,'bigdata',4500],
     ['106','akash','k',26,'flutter',2500],
     ['107','amal','k',22,'flutter',10500]]

col_name=['id','fname','lname','age','prof','salary']

df=ss.createDataFrame(data=lst,schema=col_name)
df.show()   #default 20 rows

# df.show(3)  only print first 3 rows
df.printSchema()
print(df.count())