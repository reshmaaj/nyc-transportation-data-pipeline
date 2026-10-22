# NYC Transportation Data Pipeline

A batch data engineering pipeline that processes **NYC Yellow Taxi trip data** using Python, PostgreSQL, SQL, and PySpark.

## Pipeline

```text
Raw Parquet → Pandas Cleaning → Clean Parquet → PostgreSQL → SQL Analytics
                                      ↓
                                   PySpark
```

## Tech Stack

- Python / Pandas
- PostgreSQL / SQL
- Parquet / PyArrow
- PySpark
- Git / GitHub

## What This Project Does

- Processes monthly NYC Yellow Taxi Parquet files
- Cleans and validates trip data
- Loads data into PostgreSQL using bulk `COPY`
- Uses metadata to prevent duplicate monthly loads
- Uses transactions and rollback for reliable loading
- Performs SQL analysis using joins, CTEs and window functions
- Uses PySpark for Parquet processing, joins and aggregations

## Data Processed

| Month | Raw Rows | Clean Rows |
|---|---:|---:|
| Jan 2026 | 3,724,889 | 3,678,342 |
| Feb 2026 | 3,399,866 | 3,357,962 |

**7,036,304 total rows loaded into PostgreSQL.**

## Project Structure

```text
├── src/                  # Python ETL and PySpark scripts
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── requirements.txt
└── README.md
```

## Key Concepts

**Batch ETL · Data Cleaning · Parquet · PostgreSQL Bulk Loading · Incremental Loading · Idempotency · SQL Analytics · PySpark**