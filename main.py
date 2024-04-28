import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
# from tables.people_table import *
# from tables.phones_table import *
from tables.dish_table import *
from tables.cath_table import *

class Main:
    
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        # pt = PeopleTable()
        # pht = PhonesTable()
        cth = CathTable()
        d = DishTable()
        # pt.create()
        # pht.create()
        cth.create()
        d.create()
        return

    def db_insert_somethings(self):
        # pt = PeopleTable()
        # pht = PhonesTable()
        # pt.insert_one(["Test", "Test", "Test"])
        # pt.insert_one(["Test2", "Test2", "Test2"])
        # pt.insert_one(["Test3", "Test3", "Test3"])
        # pht.insert_one([1, "123"])
        # pht.insert_one([2, "123"])
        # pht.insert_one([3, "123"])
        cth = CathTable()
        dsh = DishTable()
        
        cth.insert_one(["Завтрак"])
        cth.insert_one(["Обэд"])
        cth.insert_one(["Ужин"])
        
        dsh.insert_one([1, "10 minutes", "Яичница", "Взбить яйца, нарезать помидоры, обжарить их вместе."])
        dsh.insert_one([1, "20 minutes", "Блины", "Замесить тесто, да пожарить. ©️ Никита Сергеич"])
        dsh.insert_one([2, "2 hours", "Хлэб", "Почти, как блины, но не совсем."])
        dsh.insert_one([3, "40 minutes", "Паста", "Почувствуй себя итальянцем"])
        
    def db_drop(self):
        # pht = PhonesTable()
        # pt = PeopleTable()
        cth = CathTable()
        d = DishTable()
        # pht.drop()
        # pt.drop()
        d.drop()
        cth.drop()
        return

#     def show_main_menu(self):
#         menu = """Добро пожаловать! 
# Основное меню (выберите цифру в соответствии с необходимым действием): 
#     1 - просмотр людей;
#     2 - сброс и инициализация таблиц;
#     9 - выход."""
#         print(menu)
#         return
    def show_main_menu(self):
        menu = """Привутствуем в меню, выберите действие:
        1 - просмотр категорий;
        2 - сброс и инициализация БД;
        9 - выход;"""
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
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step
            
    def show_people(self):
        self.person_id = -1
        menu = """Просмотр списка блюд!
№\tНазвание\tВремя приготовления\tКатегория"""
        print(menu)
        lst = DishTable().all()
        for i in lst:
            print(str(i[3]) + "\t" + str(i[2]) + "\t\t" + str(i[1]) + "\t\t\t" + str(i[0]))
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление нового человека;
    4 - удаление человека;
    5 - просмотр телефонов человека;
    9 - выход."""
        print(menu)
        return
    
    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_people()
                next_step = self.read_next_step()
                current_menu = self.after_show_people(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_person()
                current_menu = "1"
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()

# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
# m.test()
m.main_cycle()


    # def after_show_people(self, next_step):
    #     while True:
    #         if next_step == "4":
    #             print("Пока не реализовано!")
    #             return "1"
    #         elif next_step == "6" or next_step == "7":
    #             print("Пока не реализовано!")
    #             next_step = "5"
    #         elif next_step == "5":
    #             next_step = self.show_phones_by_people()
    #         elif next_step != "0" and next_step != "9" and next_step != "3":
    #             print("Выбрано неверное число! Повторите ввод!")
    #             return "1"
    #         else:
    #             return next_step

    # def show_add_person(self):
    #     # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
    #     data = []
    #     data.append(input("Введите имя (1 - отмена): ").strip())
    #     if data[0] == "1":
    #         return
    #     while len(data[0].strip()) == 0:
    #         data[0] = input("Имя не может быть пустым! Введите имя заново (1 - отмена):").strip()
    #         if data[0] == "1":
    #             return
    #     data.append(input("Введите фамилию (1 - отмена): ").strip())
    #     if data[1] == "1":
    #         return
    #     while len(data[1].strip()) == 0:
    #         data[1] = input("Фамилия не может быть пустой! Введите фамилию заново (1 - отмена):").strip()
    #         if data[1] == "1":
    #             return
    #     data.append(input("Введите отчество (1 - отмена):").strip())
    #     if data[2] == "1":
    #         return
    #     PeopleTable().insert_one(data)
    #     return

    
    # def show_phones_by_people(self):
    #     if self.person_id == -1:
    #         while True:
    #             num = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
    #             while len(num.strip()) == 0:
    #                 num = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
    #             if num == "0":
    #                 return "1"
    #             person = PeopleTable().find_by_position(int(num))
    #             if not person:
    #                 print("Введено число, неудовлетворяющее количеству людей!")
    #             else:
    #                 self.person_id = int(person[1])
    #                 self.person_obj = person
    #                 break
    #     print("Выбран человек: " + self.person_obj[2] + " " + self.person_obj[0] + " " + self.person_obj[3])
    #     print("Телефоны:")
    #     lst = PhonesTable().all_by_person_id(self.person_id)
    #     for i in lst:
    #         print(i[1])
    #     menu = """Дальнейшие операции:
    # 0 - возврат в главное меню;
    # 1 - возврат в просмотр людей;
    # 6 - добавление нового телефона;
    # 7 - удаление телефона;
    # 9 - выход."""
    #     print(menu)
    #     return self.read_next_step()


    