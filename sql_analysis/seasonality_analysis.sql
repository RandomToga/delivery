-- Создаем CTE (временный результат для сложного запроса)
WITH MonthlyData AS (
    SELECT
        -- Извлекаем месяц из даты заказа
        EXTRACT(MONTH FROM Order_DateTime) AS Order_Month,
        COUNT(Order_ID) AS Total_Orders,
        AVG(Delivery_Time) AS Avg_Delivery_Time
    FROM delivery_dataset
    GROUP BY EXTRACT(MONTH FROM Order_DateTime)
)

-- Основной запрос, который использует нашу CTE
SELECT
    Order_Month,
    Total_Orders,
    Avg_Delivery_Time,
    -- Сравниваем среднее время доставки с общим средним по всем месяцам
    Avg_Delivery_Time - (SELECT AVG(Avg_Delivery_Time) FROM MonthlyData) AS Time_Difference_From_Overall_Avg
FROM MonthlyData
ORDER BY Order_Month;