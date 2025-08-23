-- самые популярные маршруты
-- для конфиденциальности данных в датасете amazon заменил координаты абстрактными
WITH Route_Counts AS (
    SELECT 
        -- Объединяем координаты магазина и точки выдачи в уникальный идентификатор маршрута
        CONCAT(ROUND(store_latitude::numeric, 2), ', ', ROUND(store_longitude::numeric, 2), 
               ' -> ', 
               ROUND(drop_latitude::numeric, 2), ', ', ROUND(drop_longitude::numeric, 2)) AS route_path,
        COUNT(order_id) AS number_of_orders,
        AVG(delivery_time) AS avg_delivery_time
    FROM delivery_dataset
    GROUP BY store_latitude, store_longitude, drop_latitude, drop_longitude
)
SELECT 
    route_path,
    number_of_orders,
    avg_delivery_time,
    -- Ранжируем маршруты по популярности
    RANK() OVER (ORDER BY number_of_orders DESC) AS popularity_rank
FROM Route_Counts
ORDER BY number_of_orders DESC
LIMIT 10;