import pandas as pd
import sys
import io

#import numpy as np
#from datetime import timedelta

def load_and_clean_data(filepath):
    """Загрузка и очистка данных"""
    # Загрузка данных
    df = pd.read_csv(filepath)
    
    # Проверка уникальности Order_ID
    assert df["Order_ID"].nunique() == len(df), "Обнаружены дубликаты Order_ID" # assert условие, "сообщение"
    df['Order_ID'] = df['Order_ID'].astype('string')
    

    # Agent_Age: фильтрация нереалистичных значений
    df = df[df['Agent_Age'].between(14, 80)]
    df['Agent_Age'] = df['Agent_Age'].astype('int8')
    
    # Agent_Rating: удаление значений >5.0 и заполнение пропусков
    df = df[df['Agent_Rating'] <= 5.0]
    df['Agent_Rating'] = df['Agent_Rating'].fillna(df['Agent_Rating'].median()).astype('float32')
    
    # Обработка геоданных
    coord_cols = ['Store_Latitude', 'Store_Longitude', 'Drop_Latitude', 'Drop_Longitude']
    df[coord_cols] = df[coord_cols].astype('float32')
    
    # Удаление нереальных координат
    df = df[
        df['Store_Latitude'].between(-90, 90) & 
        df['Store_Longitude'].between(-180, 180) &
        df['Drop_Latitude'].between(-90, 90) & 
        df['Drop_Longitude'].between(-180, 180)
    ]
    
    # Обработка временных данных
    # Объединение даты и времени заказа
    df['Order_DateTime'] = pd.to_datetime(
        df['Order_Date'] + ' ' + df['Order_Time'],
        errors='coerce'
    )
    df.drop(['Order_Date', 'Order_Time'], axis=1, inplace=True)
    
    # Преобразование времени забора
    df['Pickup_Time'] = pd.to_timedelta(df['Pickup_Time'])
    
    # Удаление строк с невалидными временными данными
    df.dropna(subset=['Order_DateTime'], inplace=True)
    
    # Фильтрация временных аномалий
    # Время забора не может быть раньше времени заказа
    df = df[df['Order_DateTime'] + df['Pickup_Time'] >= df['Order_DateTime']]
    
    # Delivery_Time не может быть отрицательным или слишком большим
    df = df[df['Delivery_Time'].between(5, 1440)]  # от 5 мин до 24 часов
    df['Delivery_Time'] = df['Delivery_Time'].astype('int16')
    # Категориальные данные
    cat_cols = ['Weather', 'Traffic', 'Vehicle', 'Area', 'Category']
    for col in cat_cols:
        df[col] = df[col].astype('category')
    
    return df

def info_data(df):
    print(f"Осталось записей: {len(df)}")
    print("\nТипы данных:")
    print(df.info())

# Настройка кодировки вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# если файл запускается напрямую
if __name__ == "__main__":
    filepath = r"C:\Users\User\Documents\GitHub\delivery\data\amazon_delivery.csv"
    cleaned_df = load_and_clean_data(filepath)
    
    info_data(cleaned_df)
    
    # Сохранение результата
    cleaned_df.to_csv("data/cleaned_delivery_data.csv", index=False)
    print("\nДанные успешно сохранены в cleaned_delivery_data.parquet")