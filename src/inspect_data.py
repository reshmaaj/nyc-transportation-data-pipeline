from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("NYC Taxi Lakehouse")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

trip_path = "data/bronze/yellow_tripdata_2026-01.parquet"
zone_path = "data/bronze/taxi_zone_lookup.csv"

trips_df = spark.read.parquet(trip_path)

zones_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(zone_path)
)

print("\n--- TRIP SCHEMA ---")
trips_df.printSchema()

print("\n--- TRIP SAMPLE ---")
trips_df.show(5, truncate=False)

print("\n--- TOTAL TRIPS ---")
print(trips_df.count())

print("\n--- TRIP COLUMNS ---")
print(trips_df.columns)

print("\n--- TAXI ZONE SCHEMA ---")
zones_df.printSchema()

print("\n--- TAXI ZONE SAMPLE ---")
zones_df.show(10, truncate=False)

print("\n--- TOTAL TAXI ZONES ---")
print(zones_df.count())

spark.stop()