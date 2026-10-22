select count(*)
from taxi_trips;

select 
	date_trunc('month', pickup_date) as month,
	count(*) as total_trips
from taxi_trips
group by date_trunc('month', pickup_date)
order by month;

SELECT
    DATE_TRUNC('month', pickup_date) AS month,
    COUNT(*) AS total_trips,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_trip_amount
FROM taxi_trips
WHERE total_amount > 0
GROUP BY DATE_TRUNC('month', pickup_date)
ORDER BY month;

SELECT
    z.borough,
    z.zone,
    COUNT(*) AS total_pickups
FROM taxi_trips t
JOIN taxi_zones z
    ON t.pickup_location_id = z.location_id
GROUP BY
    z.borough,
    z.zone
ORDER BY total_pickups DESC
LIMIT 10;

SELECT
    CASE
        WHEN trip_distance < 2 THEN 'Short'
        WHEN trip_distance < 5 THEN 'Medium'
        WHEN trip_distance < 15 THEN 'Long'
        ELSE 'Very Long'
    END AS trip_category,

    COUNT(*) AS total_trips,
	
    ROUND(AVG(total_amount), 2) AS avg_amount

FROM taxi_trips
GROUP BY trip_category
ORDER BY total_trips DESC;

SELECT
    EXTRACT(HOUR FROM pickup_datetime) AS pickup_hour,
    COUNT(*) AS total_trips
FROM taxi_trips
GROUP BY pickup_hour
ORDER BY pickup_hour;

SELECT DISTINCT payment_type
FROM taxi_trips
ORDER BY payment_type;

SELECT
    CASE payment_type
        WHEN 1 THEN 'Credit Card'
        WHEN 2 THEN 'Cash'
        WHEN 3 THEN 'No Charge'
        WHEN 4 THEN 'Dispute'
        WHEN 5 THEN 'Unknown'
        WHEN 6 THEN 'Voided Trip'
        ELSE 'Other'
    END AS payment_method,
    COUNT(*) AS total_trips,
    ROUND(AVG(total_amount), 2) AS avg_trip_amount,
    ROUND(AVG(tip_amount), 2) AS avg_tip
FROM taxi_trips
GROUP BY payment_method
ORDER BY total_trips DESC;

WITH zone_stats AS (
    SELECT
        z.borough,
        z.zone,
        COUNT(*) AS total_trips,
        AVG(t.total_amount) AS avg_trip_amount
    FROM taxi_trips t

    JOIN taxi_zones z
        ON t.pickup_location_id = z.location_id
    WHERE t.total_amount > 0
    GROUP BY
        z.borough,
        z.zone
)

SELECT
    borough,
    zone,
    total_trips,
    ROUND(avg_trip_amount, 2) AS avg_trip_amount
FROM zone_stats
WHERE total_trips >= 10000
ORDER BY avg_trip_amount DESC
LIMIT 10;

WITH zone_stats AS (
    SELECT
        z.borough,
        z.zone,
        COUNT(*) AS total_trips,
        AVG(t.total_amount) AS avg_trip_amount
    FROM taxi_trips t
    JOIN taxi_zones z
        ON t.pickup_location_id = z.location_id
    WHERE t.total_amount > 0
    GROUP BY
        z.borough,
        z.zone
)

SELECT
    borough,
    zone,
    total_trips,
    ROUND(avg_trip_amount, 2) AS avg_trip_amount
FROM zone_stats
WHERE total_trips >= 10000
ORDER BY avg_trip_amount DESC
LIMIT 10;

WITH zone_counts AS (
    SELECT
        z.borough,
        z.zone,
        COUNT(*) AS total_trips
    FROM taxi_trips t
    JOIN taxi_zones z
        ON t.pickup_location_id = z.location_id
    GROUP BY
        z.borough,
        z.zone
),

ranked_zones AS (
    SELECT
        borough,
        zone,
        total_trips,

        RANK() OVER (
            PARTITION BY borough
            ORDER BY total_trips DESC
        ) AS zone_rank
		
    FROM zone_counts
)

SELECT *
FROM ranked_zones
WHERE zone_rank <= 3
ORDER BY borough, zone_rank;

WITH monthly_trips AS (
    SELECT
        DATE_TRUNC('month', pickup_date) AS month,
        COUNT(*) AS total_trips
    FROM taxi_trips
    GROUP BY DATE_TRUNC('month', pickup_date)
)

SELECT
    month,
    total_trips,

    LAG(total_trips) OVER (  -- LAG gives the value from the previous row
        ORDER BY month
    ) AS previous_month_trips

FROM monthly_trips
ORDER BY month;
