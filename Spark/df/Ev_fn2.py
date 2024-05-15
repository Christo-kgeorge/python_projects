#max()

#newdfname-=olddfname.groupby('colname').max('colname')

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
ss=SparkSession.builder.master('local[1]').appName('jan').getOrCreate()
df=ss.read.csv('/home/ckg/Downloads/Temperature',sep=' ',header=None,inferSchema=True)
df.show()

df1=df.withColumnRenamed('_c0','year') \
      .withColumnRenamed('_c1','temp')
df1.show()

df2=df1.groupby('year').sum('temp')
df2.show()

df3=df1.groupby('year').avg('temp')     #avg and mean are same
df3.show()

df4=df1.groupby('year').min('temp')
df4.show()

df5=df1.groupby('year').mean('temp')
df5.show()

# missing value
df1.select(*(sum(col(c).isNull().cast("int")).alias(c) for c in df1.columns)).show()