from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("spark-pi-check").getOrCreate()
sc = spark.sparkContext

n = 100000
import random
count = sc.parallelize(range(n)).map(lambda _: 1 if random.random()**2 + random.random()**2 <= 1 else 0).sum()
print("Pi ≈", 4.0 * count / n)

spark.stop()