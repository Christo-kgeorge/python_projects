from pyspark.sql import SparkSession
from pyspark.sql.functions import *
ss=SparkSession.builder.master('local[1]').appName('jan').getOrCreate()
df=ss.read.csv('/home/ckg/Downloads/customer1.txt',sep=',',header=None,inferSchema=True)
df.show()


df1=df.withColumnRenamed('_c0','id') \
      .withColumnRenamed('_c1','fname') \
      .withColumnRenamed('_c2','lname') \
      .withColumnRenamed('_c3','age') \
      .withColumnRenamed('_c4','prof') \
      .withColumnRenamed('_c5','loc')
df1.show()

df2=df1.count()
print(df2)

df3=df1.distinct()
df3.show()
df4=df3.count()        #df3.count()
print(df4)

df5=df1.orderBy('age',ascending=False) \
       .select('fname','lname','prof','loc')
df5.show(10)

df6=df1.orderBy('age') \
       .select('fname','lname','prof','loc')
df6.show(5)

df7=df1.groupby('loc').count() \
       .orderBy('count',ascending=False)
df7.show()

df8=df1.filter(col('loc')=='australia')
df8.show()

df9=df1.groupby('age').count() \
       .orderBy('count',ascending=False)
df9.show()

df10=df1.groupby('prof').count() \
       .orderBy('count',ascending=False)
df10.show()

df11=df1.filter(col('loc')=='india')
df11.show()

df12=df11.count()
print(df12)

df13=df11.groupby('prof').count() \
       .orderBy('count',ascending=False)
df13.show()

df14=df11.orderBy('age',ascending=False) \
       .select('fname','lname','prof','age')
df14.show(3)

df15=df11.orderBy('age') \
       .select('fname','lname','prof','age')
df15.show(3)

df16=df11.filter(col('age')>40)
df16.show()

df17=df11.filter((col('age')>30) & (col('age')<40))
df18=df17.groupby('prof').count() \
         .orderBy('count',ascending=False)
df18.show()

df19=df1.filter(col('loc')=='us')
df20=df19.count()
print(df20)

df20=df19.groupby('age').count() \
         .orderBy('count',ascending=False)
df20.show()

df21=df19.groupby('prof').count() \
       .orderBy('count',ascending=False)
df21.show()


df22=df19.filter((col('prof')=='Civil engineer') & (col('age')>30))
df22.show()