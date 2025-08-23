-- Среднее время доставки для каждого типа транспорта (Vehicle). Какой транспорт самый быстрый? Самый медленный?
SELECT
    vehicle,
    AVG(delivery_time) AS avg_delivery_time,
    -- Оконная функция: присваиваем ранги (1-е место у того, у кого  среднее время доставки меньше всех)
     RANK() OVER (ORDER BY AVG(delivery_time) ASC) AS rank_of_vehicle_by_time,
    -- 
    ROUND(COUNT(vehicle) * 100.0 / SUM(COUNT(vehicle)) OVER (), 2) AS percent_of_used_vehicle
FROM delivery_dataset
GROUP BY vehicle
ORDER BY avg_delivery_time ASC;