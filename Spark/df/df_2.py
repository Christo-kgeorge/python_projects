from pyspark.sql import SparkSession
from pyspark.sql.functions import *
ss=SparkSession.builder.master('local[1]').appName('jan').getOrCreate()
#id,fnam,lanme,sub1,sub2,sub3
lst=[['101','aswin','h',38,31,35],
     ['102','gautham','h',44,34,50],
     ['103','amith','p',48,25,45],
     ['104','alan','c',40,45,35],
     ['105','jovel','j',39,30,45],
     ['106','akash','k',37,48,38],
     ['107','amal','k',34,36,46]]

col_name=['id','fname','lname','sub1','sub2','sub3']

df=ss.createDataFrame(data=lst,schema=col_name)
df.show()

print("*"*100)
# how to add a new column

df1=df.withColumn('coll_name',lit('MGM')) \
      .withColumn('Total_marks',col('sub1')+col('sub2')+col('sub3')) \
      .withColumnRenamed('id','roll_no')
df1.show()