from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg, round


# Create Spark session
spark = (
    SparkSession.builder
    .appName("NYC Taxi Analysis")
    .master("local[*]")
    .getOrCreate()
)


# Read cleaned taxi trip data
trips_df = spark.read.parquet(
    "data/silver/yellow_tripdata_2026-01_clean.parquet"
)

print("Total trips:", trips_df.count())


# Read taxi zone lookup
zones_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/bronze/taxi_zone_lookup.csv")
)


# Join trips with pickup zone information
trips_with_zones = trips_df.join(
    zones_df,
    trips_df["PULocationID"] == zones_df["LocationID"],
    "left"
)


# Calculate borough-level trip statistics
borough_summary = (
    trips_with_zones
    .groupBy("Borough")
    .agg(
        count("*").alias("total_trips"),
        round(avg("trip_distance"), 2).alias("avg_distance"),
        round(avg("total_amount"), 2).alias("avg_trip_amount")
    )
    .orderBy("total_trips", ascending=False)
)

borough_summary.show()

spark.stop()
