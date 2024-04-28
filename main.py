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
            return next_step;
            
    def show_cath(self):
        self.cath_id = -1
        menu = """Просмотр списка категорий!
№\tНазвание\n------------------------"""
        print(menu)
        lst = CathTable().all()
        for i in lst:
            print(str(i[1]) + "\t" + str(i[0]))
        menu = """------------------------\nДальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление новой категории;
    4 - удаление категории;
    5 - просмотр блюд в категории;
    9 - выход."""
        print(menu)
        return
    
    def after_show_cath(self, next_step):
        while True:
            if next_step == "4":
                CathTable().delete(input('Введите название удаляемой категории: '))
                return "1"
            elif next_step == "6" or next_step == "7":
                print("Пока не реализовано!")
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_dish_in_cath()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def add_cath(self):
        data = []
        data.append(input("Введите название (1 - отмена): ").strip())
        if data[0] == "1":
            return
        while (len(data[0].strip()) == 0)or(len(data[0].strip()) > 32):
            if (len(data[0].strip()) > 32):
                data[0] = input("Название слишком длинное! Введите название заново (1 - отмена):").strip()
                if data[0] == "1":
                    return
            else:
                data[0] = input("Название не может быть пустым! Введите название заново (1 - отмена):").strip()
                if data[0] == "1":
                    return
            CathTable().insert_one(data)
        return
    
    def show_dish_in_cath(self):
        if self.cath_id == -1:
            while True:
                name = input("Укажите название категории для вывода блюд (0 - отмена):")
                while len(name.strip()) == 0:
                    name = input("Пустая строка. Повторите ввод! Укажите название категории для вывода блюд (0 - отмена):")
                if name == "0":
                    return "1"
                cath = CathTable().find_by_position(int(name))
                if not cath:
                    print("Введено неверное название!")
                else:
                    self.cath_id = int(cath[1])
                    self.cath_obj = cath
                    break
        print("Выбрана категория: " + self.cath_obj[1])
        print("Блюда:")
        lst = DishTable().all_by_cath_id(self.cath_id)
        for i in lst:
            print(i[1])
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр категорий;
    6 - добавление нового блюда;
    7 - удаление блюда;
    9 - выход."""
        print(menu)
        return self.read_next_step()

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_cath()
                next_step = self.read_next_step()
                current_menu = self.after_show_cath(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.add_cath()
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