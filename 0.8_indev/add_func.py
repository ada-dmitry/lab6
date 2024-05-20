import re
import os

def input_time_format(name): 
    time = [] 
    output = ''
    print(f'Процесс добавления блюда: {name}\nВведите время приготовления сначала в часах, потом в минутах')
    
    while True:
        ins_time = validate_input(f'Введите кол-во часов [0 <= x <= 23] (-1 - для отмены): ',\
            0, 23)
        if(ins_time==''): 
            return -1
        else:
            time.append(ins_time)
            break
        
    while True:
        ins_time = validate_input(f'Введите кол-во минут [0 <= x <= 59] (-1 - для отмены): ',\
            0, 59)
        if(ins_time==''): 
            return -1
        else:
            time.append(ins_time)
            break
    if(time[0]==1):
        output += f"1 hour "
    elif(time[0]>1):
        output += f"{time[0]} hours "
    else:
        pass
    if(time[1]==1):
        output += f"1 minute"
    elif(time[1]>1):
        output += f"{time[0]} minutes"
    else:
        pass
    return output

# def validate_time_format(input_str):
    
#     """
#     Функция проверки подходящего формата для ввода времени в interval

#     Args:
#         input_str (str): входная строка для проверки

#     Returns:
#         bool: Булевое значение, которое характеризует валидность вводимых строк
#     """    
#     # Регулярное выражение для проверки формата
#     pattern = re.compile(r"""^(-)?(?:(?P<hour>d+):)?(?P<minute>d+):(?P<second>d+(.d+)?)$""")
#     # Проверка соответствия регулярному выражению
#     match = re.match(pattern, input_str)
    
#     if match:
#         return True
#     # Если формат некорректный, возвращаем False
#     return False

def validate_input(prompt, min_value, max_value):
    """Проверка ввода для выбора номера строки

    Args:
        prompt (string): "Промт" или запрос пользователю
        min_value (int): Нижняя граница, по умолчанию 0
        max_value (int): Верхняя граница

    Returns:
        int: Либо число, введенное пользователем, либо -1 для выхода
    """    
    while True:
        user_input = input(prompt).strip()
        try:
            value = int(user_input)
            if min_value <= value <= max_value and value != -1:
                return value
            elif value == -1:
                return -1
            else:
                print(f"Введенное значение должно быть в диапазоне от {min_value} до {max_value}")
        except ValueError:
            print("Введенное значение должно быть числом.")
            



# test1 = 'erhwogngonwro'
# test2 = '1 minute'
# test3 = '2 hours 3 minutes'

# print(validate_time_format(test1), validate_time_format(test2), validate_time_format(test3))

def add_zero_before(old_index: str, max_len: str) -> str:
    """Функция для "красивого" вывода индексов

    Args:
        old_index (str): текущий индекс для вывода
        max_len (int): максимальная длина индексов
    
    Returns:
        new_index (str): окончательная версия индекса
    """    
    ln = len(old_index)
    new_index = old_index[:]
    for i in range(max_len-ln):
        new_index = '0' + new_index
    return new_index
        
    
def cls():
    # Закомментировать строку ниже, если нужно выключить очистку терминала
    # os.system('cls')
    return