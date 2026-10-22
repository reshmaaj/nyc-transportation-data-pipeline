import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("data/bronze/taxi_zone_lookup.csv")

print("Rows to load:", len(df))
print(df.head())

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

# Insert each taxi zone
for _, row in df.iterrows():  # df.iterrows() goes through the DataFrame one row at a time
    cursor.execute(
        """
        INSERT INTO taxi_zones (
            location_id,
            borough,
            zone,
            service_zone
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (location_id) DO NOTHING;
        """,
        (
            row["LocationID"],
            row["Borough"],
            row["Zone"],
            row["service_zone"]
        )
    )

conn.commit()

cursor.close()
conn.close()

print("Taxi zones loaded successfully!")