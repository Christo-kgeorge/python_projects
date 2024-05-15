from pyspark.sql import SparkSession
from pyspark.sql.functions import *
ss=SparkSession.builder.master('local[1]').appName('jan').getOrCreate()
df=ss.read.csv('/home/ckg/Downloads/sample4.txt',sep=',',header=None,inferSchema=True)
df.show()



df.printSchema()


df1=df.withColumnRenamed('_c0','id') \
      .withColumnRenamed('_c1','fname') \
      .withColumnRenamed('_c2','lname') \
      .withColumnRenamed('_c3','age') \
      .withColumnRenamed('_c4','phno') \
      .withColumnRenamed('_c5','loc')
df1.show()


#only needed columns  we use 'select'

df2=df1.select('fname','lname','age','phno')
df2.show()

#filter :-- to get data which satisfies condition

#newdfname=olddfname.filter(col('colname')condition)

#age above 23

df3=df1.filter(col('age')>23)
df3.show()


df4=df1.filter(col('age')==21) \
       .select('fname','lname','phno','loc')
df4.show()


df5=df1.filter(col('loc')=='Chennai') \
       .select('fname','lname','age','phno')
df5.show()

df6=df1.filter((col('age')>23)&(col('loc')=='Chennai')) \
       .select('fname','lname','age','phno')
df6.show()



#orderby

df7=df1.orderBy('age',ascending=False)
df7.show()
