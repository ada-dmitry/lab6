import sys

sys.path.append('tables')

from project_config import *
from dbconnection import *
from cathegory_table import *
from dish_table import *


class Main:
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        ct = CathegoryTable()
        dt = DishTable()
        ct.create()
        dt.create()
        return

    def db_insert_somethings(self):
        ct = CathegoryTable()
        dt = DishTable()
        ct.insert_one(["Салат"])
        ct.insert_one(["Второе"])
        ct.insert_one(["Суп"])
        dt.insert_one(["Борщ", "120", "Сварить супчик", 3])
        dt.insert_one(["Домашний салат", "15", "Настругать салатик", 1])
        dt.insert_one(["Жаркое", "60", "Нажарить на славу", 2])
        dt.insert_one(["Цезарь", "40", "Настругать салатик с курицей", 1])

    def db_drop(self):
        ct = CathegoryTable()
        dt = DishTable()
        ct.drop()
        dt.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр всех категорий;
    2 - сброс и инициализация таблиц;
    3 - просмотр всех блюд;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        if not next_step.isdigit():
            print("Неверный тип данных! Введите число!")
            return "0"
        elif next_step != "1" and next_step != "9" and next_step != "3":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_cathegory(self):
        menu = """Просмотр категорий!
№\tНазвание"""
        print(menu)
        allCathegory = CathegoryTable().all()
        self.max_cath_index = len(allCathegory)
        for i in allCathegory:
            print(str(i[0]) + "\t" + str(i[1]))
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    4 - добавление новой категории;
    5 - удаление категории;
    6 - изменить название категории;
    9 - выход."""
        print(menu)
        return

    def show_dish(self):
        menu = """Просмотр блюд!
Формат: № ; Название ; Время приготовления ; Мануал ; Номер категории"""
        print(menu)
        allDish = DishTable().all()
        for i in allDish:
            print(str(i[0]) + " ; " + str(i[1]) + " ; " + str(i[2]) + " ; " + str(i[3]) + " ; " + str(i[4]))
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    1 - просмотр блюд по номеру категории;
    2 - удаление блюда;
    3 - добавление блюда;
    9 - выход."""
        print(menu)
        return

    def after_show_dish(self, next_step):
        while True:
            if next_step == "1":
                self.all_dish_by_cathegory()
                return "0"
            elif next_step == "2":
                self.del_dish()
                return "3"
            elif next_step == "3":
                self.insert_dish()
                return "3"
            elif next_step != "0" and next_step != "9":
                print("Выбрано неверное число! Повторите ввод!")
                next_step = self.read_next_step()
            else:
                return next_step

    def all_dish_by_cathegory(self):
        cathegory_number = input("Введите номер категории(enter - отмена): ").strip()
        if cathegory_number == "":
            return
        try:
            cathegory_number = int(cathegory_number)
        except ValueError:
            print("Неверный тип. Ожидается число")
            return
        txt = """"Просмотр блюд!
Формат: № ; Название ; Время приготовления ; Мануал ; Номер категории"""
        print(txt)
        allDish = DishTable().get_all_by_cathegory_number(cathegory_number)
        for i in allDish:
            print(str(i[0]) + " ; " + str(i[1]) + " ; " + str(i[2]) + " ; " + str(i[3]) + " ; " + str(i[4]))


    def del_dish(self):
        dish_id = input("Введите № блюда для удаления: ").strip()
        try:
            dish_id = int(dish_id)
            if dish_id > 0:
                DishTable().delete_one(dish_id)
            else:
                print("Неверное значение. Ожидается целое положительное число")
                return
        except ValueError:
            print("Неверный тип. Ожидается число")
            return
        dish_table = DishTable()
        if not dish_table.exist_by_number(dish_id):
            print("Указанный номер блюда не найден. Попробуйте заново")
            return

        dish_table.delete_one(dish_id)
        print("Блюдо успешно удалено")


    def insert_dish(self):
        data = []

        data.append(input("Введите имя блюда(enter - отмена): ").strip())
        while len(data[0].strip()) > 64:
            data[0] = input("Неверная длина! Имя должно быть не пустым и не больше 64 символов. Введите имя заново (1 - отмена):").strip()
        if data[0] == "":
            print("Отмена действия")
            return

        data.append(input("Введите время приготовления в минутах(0 - отмена): ").strip())
        flag = True
        while flag:
            try:
                data[1] = int(data[1])
            except ValueError:
                data[1] = input("Неверный тип. Ожидается число. Введите число заново (0 - отмена):").strip()
                continue
            flag = False
        if data[1] == 0:
            return
        if data[1] < 0:
            print("Время не может быть отрицательным")
            return

        data.append(input("Введите мануал(enter - отмена): ").strip())
        #while len(data[2].strip()) == 0:
        #    data[2] = input("Неверная длина! Мануал должно быть не пустым. Введите мануал заново (enter - отмена):").strip()
        if data[2] == "":
            print("Отмена действия")
            return

        data.append(input("Введите номер категории(enter - отмена): ").strip())
        if data[3] == "":
            return
        flag = True
        while flag:
            try:
                data[3] = int(data[3])
            except ValueError:
                data[3] = input("Неверный тип. Ожидается число. Введите число заново (enter - отмена):").strip()
                if data[3] == "":
                    return
                continue
            flag = False

        if not (CathegoryTable().exist_by_number(data[3])):
            print("Указанный номер категории не найдем. Попробуйте заново")
            return
        DishTable().insert_one(data)

    def after_show_cathegory(self, next_step):
        while True:
            if next_step == "4":
                self.insert_cathegory()
                return "1"
            elif next_step == "5":
                self.del_cathegory()
                return "1"
            elif next_step == "6" :
                self.update_cathegory()
                return "1"
            elif next_step != "0" and next_step != "9":
                print("Выбрано неверное число! Повторите ввод!")
                next_step = self.read_next_step()
            else:
                return next_step

    def insert_cathegory(self):
        data = []
        data.append(input("Введите имя категории(1 - отмена): ").strip())
        while len(data[0].strip()) == 0 or len(data[0].strip())>20:
            data[0] = input("Неверная длина! Имя должно быть не пустым и не больше 20 символов. Введите имя заново (1 - отмена):").strip()
        if data[0] == "1":
            return

        CathegoryTable().insert_one(data)

    def del_cathegory(self):
        while True:
            cathegory_id = input("Введите № категории для удаления: ").strip()
            try:
                cathegory_id = int(cathegory_id)
            except ValueError:
                print("Неверный тип. Ожидается число")
                # return
            if (cathegory_id <= 0)or(cathegory_id > self.max_cath_index):
                print(f'Число должно лежать в диапазоне от 1 до {self.max_cath_index}.')
            elif not (CathegoryTable().exist_by_number(cathegory_id)):
                print("Указанный номер категории не найдем. Попробуйте заново")
                # return
            else:
                break
        DishTable().delete_all_with_cathegory_id(cathegory_id)
        CathegoryTable().delete_one(cathegory_id)
        return

    def update_cathegory(self):
        data = []
        cathegory_id = input("Введите № категории для изменения: ").strip()
        try:
            cathegory_id = int(cathegory_id)
        except ValueError:
            print("Неверный тип. Ожидается число")
            return
        if not (CathegoryTable().exist_by_number(cathegory_id)):
            print("Указанный номер категории не найдем. Попробуйте заново")
            return

        data.append(input("Введите имя категории(1 - отмена): ").strip())
        while len(data[0].strip()) == 0 or len(data[0].strip()) > 20:
            data[0] = input("Неверная длина! Имя должно быть не пустым и не больше 20 символов. Введите имя заново (1 - отмена):").strip()
        if data[0] == "1":
            return
        CathegoryTable().update(cathegory_id, data)

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while (current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_cathegory()
                next_step = self.read_next_step()
                current_menu = self.after_show_cathegory(next_step)
            elif current_menu == "3":
                self.show_dish()
                next_step = self.read_next_step()
                current_menu = self.after_show_dish(next_step)
        print("До свидания!")
        return

    def test(self):
        DbTable.dbconn.test()


m = Main()
# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
# m.test()
m.main_cycle()
