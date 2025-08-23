import psycopg2

DB_PARAMS = {
    "host": "localhost",
    "database": "delivery_db",
    "user": "postgres",
    "password": "***",
    "port": "5432"
}

conn = psycopg2.connect(**DB_PARAMS)
cursor = conn.cursor()

# Создаём таблицу (если её нет)
cursor.execute("""
CREATE TABLE IF NOT EXISTS delivery_dataset (
    Order_ID VARCHAR(50) PRIMARY KEY,
    Agent_Age SMALLINT NOT NULL,
    Agent_Rating REAL NOT NULL,
    Store_Latitude REAL NOT NULL,
    Store_Longitude REAL NOT NULL,
    Drop_Latitude REAL NOT NULL,
    Drop_Longitude REAL NOT NULL,
    Pickup_Time INTERVAL NOT NULL,
    Weather VARCHAR(50) NOT NULL,
    Traffic VARCHAR(50) NOT NULL,
    Vehicle VARCHAR(50) NOT NULL,
    Area VARCHAR(50) NOT NULL,
    Delivery_Time SMALLINT NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Order_DateTime TIMESTAMP NOT NULL
);
""")

# Загружаем CSV напрямую в PostgreSQL
with open("data/cleaned_delivery_data.csv", "r", encoding="utf-8") as f:
    cursor.copy_expert("""
        COPY delivery_dataset FROM STDIN WITH CSV HEADER DELIMITER ','
    """, f)

conn.commit()
cursor.close()
conn.close()
print("🚀 Данные напрямую загружены из CSV в PostgreSQL")
