from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.getOrCreate()

name = input("Enter player name: ").lower()

df = spark.read.csv("/app/data/final_cricket_data.csv", header=True)

result = df.filter(col("Player").rlike(name)) \
    .groupBy("Player") \
    .sum("Runs_x", "Wkts", "Catches")

result.show()