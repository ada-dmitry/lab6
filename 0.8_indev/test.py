# # a = dict()

# # for i in range(1, 41, 2):
# #     for j in range(2, 41, 2):
# #         a[f"{i}"] = f"{j}"
        
# # print(a)
    
# # import psycopg2
# # from psycopg2.extras import Interval

# # def check_interval(value):
# #     try:
# #         # Попытка преобразования значения в объект Interval
# #         interval_obj = Interval(value)
# #         # Если преобразование успешно, значение относится к типу Interval
# #         return isinstance(interval_obj, Interval)
# #     except (ValueError, TypeError):
# #         # Если преобразование не удалось, значение не относится к типу Interval
# #         return False
    
# # user_input = input("Введите интервал: ")
# # if check_interval(user_input):
# #     print("Введенное значение относится к типу Interval")
# # else:
# #     print("Введенное значение не относится к типу Interval")

# import psycopg2
# from psycopg2.extras import DateTimeTZRange

# def check_interval(input_str):
#     try:
#         # Создаем объект Interval из входной строки
#         interval = DateTimeTZRange(input_str, '[]')
#     except (ValueError, psycopg2.DataError):
#         return False
#     return True
# # Примеры использования
# print(check_interval('1 day'))     # True
# print(check_interval('1:60'))      # False
# print(check_interval('P1Y2M3DT4H5M6.7S'))  # True

import this