-- Насколько погода влияет на время доставки? Посчитать среднее время доставки для каждого типа погоды на каждом транспорте (Weather)
WITH weather_avg AS (
    SELECT 
        weather,
        AVG(delivery_time) AS avg_weather_time
    FROM delivery_dataset
    GROUP BY weather
)
SELECT 
    d.weather,
    d.vehicle,
    AVG(d.delivery_time) AS avg_delivery_time
FROM delivery_dataset AS d
JOIN weather_avg AS w ON d.weather = w.weather
GROUP BY d.weather, d.vehicle, w.avg_weather_time
ORDER BY w.avg_weather_time ASC,  -- Сначала погода с наименьшим средним временем
         AVG(d.delivery_time) ASC; -- Затем транспорт от быстрого к медленному внутри погоды