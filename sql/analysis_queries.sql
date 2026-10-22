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