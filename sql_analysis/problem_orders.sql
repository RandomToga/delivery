-- Запрос на выявление заказов, которые доставляются дольше среднего времени доставки
SELECT 
    order_id,
    delivery_time,
    area,
    traffic,
    weather,
    vehicle
FROM delivery_dataset
WHERE delivery_time > (
    SELECT AVG(delivery_time)
    FROM delivery_dataset
)
ORDER BY Delivery_Time DESC;