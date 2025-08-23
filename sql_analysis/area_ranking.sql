-- Ранжирование городов/районов (Area) по количеству заказов
SELECT
    Area,
    COUNT(order_id) AS total_orders,
    -- Оконная функция: присваиваем ранги (1-е место у того, у кого больше всего заказов)
    RANK() OVER (ORDER BY COUNT(order_id) DESC) AS area_rank_by_orders,
    -- Считаем долю заказов каждого района от общего числа
    ROUND(COUNT(order_id) * 100.0 / SUM(COUNT(order_id)) OVER (), 2) AS percent_of_total_orders
FROM delivery_dataset
GROUP BY Area
ORDER BY Total_Orders DESC;