# a = dict()

# for i in range(1, 41, 2):
#     for j in range(2, 41, 2):
#         a[f"{i}"] = f"{j}"
        
# print(a)
    
# import psycopg2
# from psycopg2.extras import Interval

# def check_interval(value):
#     try:
#         # Попытка преобразования значения в объект Interval
#         interval_obj = Interval(value)
#         # Если преобразование успешно, значение относится к типу Interval
#         return isinstance(interval_obj, Interval)
#     except (ValueError, TypeError):
#         # Если преобразование не удалось, значение не относится к типу Interval
#         return False
    
# user_input = input("Введите интервал: ")
# if check_interval(user_input):
#     print("Введенное значение относится к типу Interval")
# else:
#     print("Введенное значение не относится к типу Interval")

from psycopg2 import Error
import psycopg2

def is_valid_interval(input_string):
    try:
        # Создаем соединение с базой данных
        conn = psycopg2.connect("dbname=your_database user=your_username password=your_password")
        
        # Создаем курсор для выполнения запросов
        cursor = conn.cursor()
        
        # Формируем запрос для проверки ввода
        query = f"SELECT to_interval('{input_string}');"
        
        # Выполняем запрос
        cursor.execute(query)
        
        # Получаем результаты
        result = cursor.fetchone()
        
        # Закрываем курсор и соединение
        cursor.close()
        conn.close()
        
        # Проверяем, был ли результат успешным
        if result is not None:
            return True
        else:
            return False
    except Error as e:
        print(f"Произошла ошибка: {e}")
        return False

# Примеры использования
print(is_valid_interval('10:30'))  # Выведет True
print(is_valid_interval('1:60'))  