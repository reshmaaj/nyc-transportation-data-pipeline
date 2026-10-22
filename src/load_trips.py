import os
import sys
import tempfile

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# INPUT_FILE = "data/silver/yellow_tripdata_2026-01_clean.parquet"
# SOURCE_FILE = "yellow_tripdata_2026-01.parquet"


#getting mon from cmd line args
if len(sys.argv) != 2:
    print("Usage: python src/load_trips.py YYYY-MM")
    sys.exit(1)

month = sys.argv[1]

INPUT_FILE = f"data/silver/yellow_tripdata_{month}_clean.parquet"
SOURCE_FILE = f"yellow_tripdata_{month}.parquet"


if not os.path.exists(INPUT_FILE):
    print(f"Clean file not found: {INPUT_FILE}")
    print(f"Run: python src/clean_data.py {month}")
    sys.exit(1)


conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

cursor.execute(
    """
    SELECT 1
    FROM pipeline_metadata
    WHERE file_name = %s;
    """,
    (SOURCE_FILE,)
)

already_loaded = cursor.fetchone()

if already_loaded:
    print(f"{SOURCE_FILE} has already been processed. Skipping.")
    cursor.close()
    conn.close()
    exit()


df = pd.read_parquet(INPUT_FILE)

print("Rows read:", len(df))


df = df[
    [
        "VendorID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "RatecodeID",
        "PULocationID",
        "DOLocationID",
        "payment_type",
        "fare_amount",
        "tip_amount",
        "tolls_amount",
        "total_amount",
        "congestion_surcharge",
        "Airport_fee",
        "cbd_congestion_fee",
        "trip_duration_minutes",
        "pickup_date"
    ]
].copy()


df.columns = [
    "vendor_id",
    "pickup_datetime",
    "dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "rate_code_id",
    "pickup_location_id",
    "dropoff_location_id",
    "payment_type",
    "fare_amount",
    "tip_amount",
    "tolls_amount",
    "total_amount",
    "congestion_surcharge",
    "airport_fee",
    "cbd_congestion_fee",
    "trip_duration_minutes",
    "pickup_date"
]


integer_columns = [
    "vendor_id",
    "passenger_count",
    "rate_code_id",
    "pickup_location_id",
    "dropoff_location_id",
    "payment_type"
]

for column in integer_columns:
    df[column] = df[column].astype("Int64")


with tempfile.NamedTemporaryFile(
    mode="w",
    suffix=".csv",
    delete=False,
    newline="",
    encoding="utf-8"
) as temp_file:

    temp_path = temp_file.name

    df.to_csv(
        temp_file,
        index=False,
        header=False,
        na_rep="\\N"
    )

print("Temporary CSV created.")



copy_sql = """
COPY taxi_trips (
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    rate_code_id,
    pickup_location_id,
    dropoff_location_id,
    payment_type,
    fare_amount,
    tip_amount,
    tolls_amount,
    total_amount,
    congestion_surcharge,
    airport_fee,
    cbd_congestion_fee,
    trip_duration_minutes,
    pickup_date
)
FROM STDIN
WITH (
    FORMAT CSV,
    NULL '\\N'
);
"""


try:
    with open(temp_path, "r", encoding="utf-8") as f:
        cursor.copy_expert(copy_sql, f)

    cursor.execute(
        """
        INSERT INTO pipeline_metadata (
            file_name,
            row_count
        )
        VALUES (%s, %s);
        """,
        (SOURCE_FILE, len(df))
    )

    conn.commit()

    print("Taxi trips loaded successfully!")

except Exception as e:
    conn.rollback()
    print("Load failed:", e)


finally:
    cursor.close()
    conn.close()

    if os.path.exists(temp_path):
        os.remove(temp_path)

    print("Temporary CSV removed.")