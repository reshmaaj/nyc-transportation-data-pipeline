import sys
import os
import pandas as pd


# --------------------------------
# 1. GET MONTH FROM COMMAND LINE
# --------------------------------
if len(sys.argv) != 2:
    print("Usage: python src/clean_data.py YYYY-MM")
    sys.exit(1)

month = sys.argv[1]

input_file = f"data/bronze/yellow_tripdata_{month}.parquet"
output_file = f"data/silver/yellow_tripdata_{month}_clean.parquet"


# --------------------------------
# 2. CHECK SOURCE FILE EXISTS
# --------------------------------
if not os.path.exists(input_file):
    print(f"Source file not found: {input_file}")
    sys.exit(1)


# --------------------------------
# 3. LOAD RAW DATA
# --------------------------------
df = pd.read_parquet(input_file)

print(f"\nProcessing month: {month}")
print("Raw rows:", len(df))


# --------------------------------
# 4. KEEP ONLY THE REQUESTED MONTH
# --------------------------------
month_start = pd.Timestamp(f"{month}-01")
next_month = month_start + pd.offsets.MonthBegin(1)

df = df[
    (df["tpep_pickup_datetime"] >= month_start) &
    (df["tpep_pickup_datetime"] < next_month)
]

print("After date filtering:", len(df))


# --------------------------------
# 5. REMOVE INVALID TRIP TIMES
# --------------------------------
df = df[
    df["tpep_dropoff_datetime"] >
    df["tpep_pickup_datetime"]
]

print("After trip-time filtering:", len(df))


# --------------------------------
# 6. REMOVE EXTREME DISTANCE OUTLIERS
# --------------------------------
df = df[
    df["trip_distance"] <= 100
]

print("After distance filtering:", len(df))


# --------------------------------
# 7. CREATE TRIP DURATION
# --------------------------------
df["trip_duration_minutes"] = (
    df["tpep_dropoff_datetime"] -
    df["tpep_pickup_datetime"]
).dt.total_seconds() / 60


# --------------------------------
# 8. REMOVE EXTREME TRIP DURATIONS
# --------------------------------
df = df[
    df["trip_duration_minutes"] <= 360
]

print("After duration filtering:", len(df))


# --------------------------------
# 9. CREATE PICKUP DATE
# --------------------------------
df["pickup_date"] = df["tpep_pickup_datetime"].dt.date


# --------------------------------
# 10. SAVE CLEAN DATA
# --------------------------------
df.to_parquet(
    output_file,
    index=False
)

print("\nClean rows:", len(df))
print("Clean columns:", len(df.columns))
print("Saved to:", output_file)



# import pandas as pd

# # 1. LOAD RAW DATA
# input_file = "data/bronze/yellow_tripdata_2026-01.parquet"
# df = pd.read_parquet(input_file)

# print("Raw row:", len(df))

# # 2. KEEP JANUARY RECORDS
# df = df[
#     (df["tpep_pickup_datetime"] >= "2026-01-01") &
#     (df["tpep_pickup_datetime"] < "2026-02-01")
# ]
# print("After filtering for January records:", len(df))

# # 3. REMOVE INVALID TRIP TIMES
# df = df[
#     df["tpep_dropoff_datetime"] >
#     df["tpep_pickup_datetime"]
# ]

# print("After trip-time filtering:", len(df))

# # 4. REMOVE EXTREME DISTANCE OUTLIERS
# df = df[
#     df["trip_distance"] <= 100
# ]

# print("After distance filtering:", len(df))

# # 5. CREATE TRIP DURATION
# df["trip_duration_minutes"] = (
#     df["tpep_dropoff_datetime"] -
#     df["tpep_pickup_datetime"]
# ).dt.total_seconds() / 60
# # Remove trips longer than 6 hours
# df = df[
#     df["trip_duration_minutes"] <= 360
# ]
# print("After trip-duration filtering:", len(df))

# # 6. CREATE PICKUP DATE
# df["pickup_date"] = (
#     df["tpep_pickup_datetime"].dt.date
# )

# # 7. SAVE CLEAN DATA
# output_file = "data/silver/yellow_tripdata_2026-01_clean.parquet"
# df.to_parquet(
#     output_file, 
#     index=False
#     )

# print("\nClean rows:", len(df))
# print("\nClean columns:", len(df.columns))
# print("Cleaned data saved to:", output_file)