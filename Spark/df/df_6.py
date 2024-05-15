#distinct()

# to remove duplicate rows

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
ss=SparkSession.builder.master('local[1]').appName('jan').getOrCreate()
df=ss.read.csv('/home/ckg/Downloads/sample4.txt',sep=',',header=None,inferSchema=True)
df.show()

df1=df.withColumnRenamed('_c0','id') \
      .withColumnRenamed('_c1','fname') \
      .withColumnRenamed('_c2','lname') \
      .withColumnRenamed('_c3','age') \
      .withColumnRenamed('_c4','phno') \
      .withColumnRenamed('_c5','loc')
df1.show()


df2=df1.distinct()
df2.show()

