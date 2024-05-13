import re

def validate_time_format(input_str):
    """Функция проверки подходящего формата для ввода времени в interval

    Args:
        input_str (str): входная строка для проверки

    Returns:
        bool: Булевое значение, которое характеризует валидность вводимых строк
    """    
    # Регулярное выражение для проверки формата
    pattern = r'^(\d+\s*hours?\s*)?(\d+\s*minutes?)$'
    
    # Проверка соответствия регулярному выражению
    match = re.match(pattern, input_str)
    
    if match:
        return True
    
    # Если формат некорректный, возвращаем False
    return False

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
        user_input = input(prompt)
        try:
            value = int(user_input)
            if min_value <= value <= max_value and value != 0:
                return value
            elif value == 0:
                return -1
            else:
                print(f"Введенное значение должно быть в диапазоне от {min_value} до {max_value}")
        except ValueError:
            print("Введенное значение должно быть числом.")
