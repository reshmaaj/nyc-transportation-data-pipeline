import sys
import os
import pandas as pd


#getting mon from cmd line args
if len(sys.argv) != 2:
    print("Usage: python src/clean_data.py YYYY-MM")
    sys.exit(1)

month = sys.argv[1]

input_file = f"data/bronze/yellow_tripdata_{month}.parquet"
output_file = f"data/silver/yellow_tripdata_{month}_clean.parquet"


if not os.path.exists(input_file):
    print(f"Source file not found: {input_file}")
    sys.exit(1)


df = pd.read_parquet(input_file)

print(f"\nProcessing month: {month}")
print("Raw rows:", len(df))


month_start = pd.Timestamp(f"{month}-01")
next_month = month_start + pd.offsets.MonthBegin(1)

df = df[
    (df["tpep_pickup_datetime"] >= month_start) &
    (df["tpep_pickup_datetime"] < next_month)
]

print("After date filtering:", len(df))


df = df[
    df["tpep_dropoff_datetime"] >
    df["tpep_pickup_datetime"]
]

print("After trip-time filtering:", len(df))



df = df[
    df["trip_distance"] <= 100
]

print("After distance filtering:", len(df))



df["trip_duration_minutes"] = (
    df["tpep_dropoff_datetime"] -
    df["tpep_pickup_datetime"]
).dt.total_seconds() / 60


df = df[
    df["trip_duration_minutes"] <= 360
]

print("After duration filtering:", len(df))


df["pickup_date"] = df["tpep_pickup_datetime"].dt.date


df.to_parquet(
    output_file,
    index=False
)

print("\nClean rows:", len(df))
print("Clean columns:", len(df.columns))
print("Saved to:", output_file)



# import pandas as pd

# input_file = "data/bronze/yellow_tripdata_2026-01.parquet"
# df = pd.read_parquet(input_file)

# print("Raw row:", len(df))

# df = df[
#     (df["tpep_pickup_datetime"] >= "2026-01-01") &
#     (df["tpep_pickup_datetime"] < "2026-02-01")
# ]
# print("After filtering for January records:", len(df))

# df = df[
#     df["tpep_dropoff_datetime"] >
#     df["tpep_pickup_datetime"]
# ]

# print("After trip-time filtering:", len(df))

# df = df[
#     df["trip_distance"] <= 100
# ]

# print("After distance filtering:", len(df))

# df["trip_duration_minutes"] = (
#     df["tpep_dropoff_datetime"] -
#     df["tpep_pickup_datetime"]
# ).dt.total_seconds() / 60
# # Remove trips longer than 6 hours
# df = df[
#     df["trip_duration_minutes"] <= 360
# ]
# print("After trip-duration filtering:", len(df))

# df["pickup_date"] = (
#     df["tpep_pickup_datetime"].dt.date
# )

# output_file = "data/silver/yellow_tripdata_2026-01_clean.parquet"
# df.to_parquet(
#     output_file, 
#     index=False
#     )

# print("\nClean rows:", len(df))
# print("\nClean columns:", len(df.columns))
# print("Cleaned data saved to:", output_file)