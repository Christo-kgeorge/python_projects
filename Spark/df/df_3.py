from pyspark.sql import SparkSession
from pyspark.sql.functions import *
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
df.show()

print("*"*100)
# how to add a new column

df1=df.withColumn('Designation',lit('Software_Engineer')) \
      .withColumn('Bonus',col('salary')*.1) \
      .withColumn('Total_salary',col('salary')+col('Bonus')) \
      .withColumnRenamed('fname','first_name')
df1.show()

print("*"*100)
df2=df1.drop('prof','lname')
df2.show()