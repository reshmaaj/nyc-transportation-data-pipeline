import pandas as pd

file_path = "data/silver/yellow_tripdata_2026-01_clean.parquet"

df = pd.read_parquet(file_path)

print("\n CLEAN DATASET SHAPE")
print(df.shape)

print("\n DATE RANGE")
# print(f"Start: {df['tpep_pickup_datetime'].min()}")
print("Earliest:", df["tpep_pickup_datetime"].min())
print("Latest:", df['tpep_pickup_datetime'].max())

print("\n INVALID TRIP TIMES")
invalid_times = (
        df["tpep_dropoff_datetime"]
        <= df["tpep_pickup_datetime"]
    ).sum()

print(invalid_times)


print("\n DISTANCE > 100")
print((df["trip_distance"] > 100).sum())


print("\n TRIP DURATION STATS")
print(df["trip_duration_minutes"].describe())


print("\n SAMPLE CLEAN DATA")
print(
    df[
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "trip_duration_minutes",
            "pickup_date"
        ]
    ].head()
)

print("\n TRIPS LONGER THAN 6 HOURS")

long_trips = df[
    df["trip_duration_minutes"] > 360
]

print("Count:", len(long_trips))

print(
    long_trips[
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "fare_amount",
            "total_amount",
            "trip_duration_minutes"
        ]
    ].sort_values(
        "trip_duration_minutes",
        ascending=False
    ).head(10)
)