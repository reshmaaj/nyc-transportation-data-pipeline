CREATE TABLE IF NOT EXISTS taxi_zones (
    location_id INTEGER PRIMARY KEY,
    borough VARCHAR(50),
    zone VARCHAR(100),
    service_zone VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS taxi_trips (
    trip_id BIGSERIAL PRIMARY KEY,
    vendor_id INTEGER,
    pickup_datetime TIMESTAMP NOT NULL,
    dropoff_datetime TIMESTAMP NOT NULL,
    passenger_count INTEGER,
    trip_distance DOUBLE PRECISION,
    rate_code_id INTEGER,
    pickup_location_id INTEGER,
    dropoff_location_id INTEGER,
    payment_type INTEGER,
    fare_amount NUMERIC(10,2),
    tip_amount NUMERIC(10,2),
    tolls_amount NUMERIC(10,2),
    total_amount NUMERIC(10,2),
    congestion_surcharge NUMERIC(10,2),
    airport_fee NUMERIC(10,2),
    cbd_congestion_fee NUMERIC(10,2),
    trip_duration_minutes DOUBLE PRECISION,
    pickup_date DATE
);


CREATE TABLE IF NOT EXISTS pipeline_metadata (
    file_name VARCHAR(255) PRIMARY KEY,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    row_count BIGINT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_taxi_trips_pickup_date
ON taxi_trips (pickup_date);

CREATE INDEX IF NOT EXISTS idx_taxi_trips_pickup_location
ON taxi_trips (pickup_location_id);

CREATE INDEX IF NOT EXISTS idx_taxi_trips_dropoff_location
ON taxi_trips (dropoff_location_id);