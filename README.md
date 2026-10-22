# NYC Transportation Data Pipeline

Batch data engineering pipeline built using **Python, Pandas, PostgreSQL, SQL, and PySpark** to process NYC Yellow Taxi trip data.

## Pipeline

```text
NYC TLC Parquet Data
        ↓
Python / Pandas
        ↓
Cleaning & Validation
        ↓
Clean Parquet
        ↓
PostgreSQL (Bulk COPY)
        ↓
SQL Analytics

Clean Parquet + Taxi Zone Lookup
        ↓
PySpark Join & Aggregation
```

## Tech Stack

- Python
- Pandas
- PostgreSQL
- SQL
- PyArrow / Parquet
- psycopg2
- PySpark
- Git / GitHub

## Dataset

NYC TLC Yellow Taxi Trip Records:

| Month         |  Raw Rows | Clean Rows |
| ------------- | --------: | ---------: |
| January 2026  | 3,724,889 |  3,678,342 |
| February 2026 | 3,399,866 |  3,357,962 |

**Total loaded to PostgreSQL: 7,036,304 rows**

Raw and processed datasets are excluded from the repository due to file size.

## Data Processing

The monthly cleaning pipeline:

- Filters trips to the requested month
- Removes invalid pickup/drop-off times
- Removes trips over 100 miles
- Calculates trip duration
- Removes trips longer than 360 minutes as a project-defined quality rule
- Creates a `pickup_date` field
- Saves cleaned data as Parquet

The pipeline is parameterized by month:

```bash
python src/clean_data.py 2026-01
```

## PostgreSQL Loading

Cleaned Parquet data is loaded into PostgreSQL using **COPY FROM STDIN** for efficient bulk loading.

A `pipeline_metadata` table tracks processed files. Before loading a month, the pipeline checks this table and skips files that have already been processed.

The trip load and metadata update run in the same transaction, with rollback on failure.

```bash
python src/load_trips.py 2026-01
```

## SQL Analysis

`sql/analysis_queries.sql` includes:

- Monthly trip volume and revenue
- Top pickup zones
- Hourly demand
- Payment type analysis
- CTE-based zone statistics
- Borough-level zone ranking with `RANK()`
- Month-over-month analysis with `LAG()`

## PySpark

`src/spark_basics.py` demonstrates basic Spark processing by:

- Reading cleaned Parquet data
- Reading the NYC Taxi Zone lookup
- Joining trips with pickup zones
- Aggregating trip statistics by borough

PySpark runs locally for this project.

## Project Structure

```text
nyc-transportation-data-pipeline/
├── src/
│   ├── clean_data.py
│   ├── inspect_data.py
│   ├── inspect_with_pandas.py
│   ├── load_trips.py
│   ├── load_zones.py
│   ├── spark_basics.py
│   ├── test_db_connection.py
│   └── validate_clean_data.py
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── .gitignore
├── requirements.txt
└── README.md
```

## Key Concepts

**Batch ETL • Data Cleaning • Parquet • Bulk Loading • Transactions • Incremental Loading • Idempotency • SQL Analytics • PySpark**
