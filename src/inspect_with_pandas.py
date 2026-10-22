import pandas as pd


file_path = "data/bronze/yellow_tripdata_2026-01.parquet"

df = pd.read_parquet(file_path)


print("\n FIRST 5 ROWS")
print(df.head())


print("\n DATASET SHAPE")
print(df.shape)


print("\n COLUMN NAMES")
print(df.columns.tolist())


print("\n DATA TYPES")
print(df.dtypes)

print("\n MISSING VALUES")
print(df.isnull().sum())

print("\n DUPLICATE ROWS")
print(df.duplicated().sum())

print("\n DATE RANGE")
# print(f"Start: {df['tpep_pickup_datetime'].min()}")
print("Earliest pickup:", df["tpep_pickup_datetime"].min())
print("Latest pickup:", df['tpep_pickup_datetime'].max())

print("\n PASSENGER COUNT VALUES")
print(df["passenger_count"].value_counts(dropna=False).sort_index())

print("\n TRIP DISTANCE STATS")
print(df["trip_distance"].describe())

print("\n FAIR AMOUNT STATS")
print(df["fare_amount"].describe())

print("\n TOTAL AMOUNT STATS")
print(df["total_amount"].describe())

print("\n ZERO DISTANCE TRIPS")
print((df["trip_distance"] == 0).sum())

print("\n VERY LARGE DISTANCE (> 100 MILES)")
print((df["trip_distance"] > 100).sum())


print("\n NEGATIVE FARES")
print((df["fare_amount"] < 0).sum())


print("\n ZERO FARES")
print((df["fare_amount"] == 0).sum())


print("\n NEGATIVE TOTAL AMOUNTS")
print((df["total_amount"] < 0).sum())


print("\n INVALID TRIP TIMES")
print(
    (
        df["tpep_dropoff_datetime"]
        <= df["tpep_pickup_datetime"]
    ).sum()
)


print("\n OUTSIDE JANUARY 2026")

outside_january = (
    (df["tpep_pickup_datetime"] < "2026-01-01") |
    (df["tpep_pickup_datetime"] >= "2026-02-01")
)

print(outside_january.sum())

print("\n ROWS WITH NULL PASSENGER COUNT")

print(
    df[df["passenger_count"].isnull()][
        [
            "passenger_count",
            "RatecodeID",
            "store_and_fwd_flag",
            "congestion_surcharge",
            "Airport_fee",
            "payment_type"
        ]
    ].head(10)
)