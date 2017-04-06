from pyspark.sql import SparkSession
from pyspark.sql import Row

import collections

# Create a SparkSession (Note, the config section is only for Windows!)
spark = SparkSession.builder.config("spark.some.config.option", "some-value").appName("mySparkSQL").getOrCreate()

def mapper(line):
    fields = line.split(',')
    return Row(id=str(fields[0]), state=str(fields[1]), country=str(fields[2]), stateTwo=str(fields[3]), comment=str(fields[4]))

lines = spark.sparkContext.textFile("20170405.export.top30.csv")
events = lines.map(mapper)

# Infer the schema, and register the DataFrame as a table.
schemaEvents = spark.createDataFrame(events).cache()
schemaEvents.createOrReplaceTempView("events")

# SQL can be run over DataFrames that have been registered as a table.
MichiganEvents = spark.sql("SELECT * FROM events WHERE state == 'Michigan'")

# The results of SQL queries are RDDs and support all the normal RDD operations.
for evnt in MichiganEvents.collect():
  print(evnt)

# We can also use functions instead of SQL queries:
schemaEvents.groupBy("state").count().orderBy("state").show()

spark.stop()