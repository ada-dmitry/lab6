import sys
import texts
sys.path.append('tables')

from project_config import *
from dbconnection import *

from tables.dish_table import *
from tables.cath_table import *

'''
TODO:
1) Реализовать ввод порядкового номера - done
2) Удалить проверки на "русскоязычный ввод" - done
3) Устранить SQLi с помощью санации атрибутов - done
4) UPDATE для отдельный таблиц/общий? - indev

FIXME:
'''


class Main:
    
    
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        cth = CathTable()
        d = DishTable()
        cth.create()
        d.create()
        return

    def db_insert_somethings(self):
        cth = CathTable()
        dsh = DishTable()
        
        cth.example_insert()
        dsh.example_insert()
        
    def db_drop(self):
        cth = CathTable()
        d = DishTable()
        d.drop()
        cth.drop()
        return

    def show_main_menu(self):
        menu = texts.show_main_menu_txt
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
            
    def show_cath(self):
        self.cath_id = -1
        self.cath_arr = []
        menu = texts.show_cath_1txt
        print(menu)
        lst = CathTable().all()
        
        for i in lst:
            self.cath_arr.append(str(i[0]))
            
        for i in range(len(self.cath_arr)):
            print(str(i+1) + "\t" + self.cath_arr[i])
            
        menu = texts.show_cath_2txt
        print(menu)
        return
    
    def after_show_cath(self, next_step):
        """Выбор действий после вывода категорий
        """        
        while True:
            if next_step == "4":
                x = int(input('Введите номер удаляемой категории(0 - для отмены): '))
                if (x == 0):
                    return "1"
                else:
                    CathTable().delete(self.cath_arr[x-1])
                return "1"
            
            elif next_step == "6": #Добавление блюда в категорию
                DishTable().insert_dishone(self.cath_id)
                next_step = "5"
                
            elif next_step == "7":#Удаление блюда из категории
                x = int(input('Введите номер удаляемого блюда (0 - для отмены): '))
                if(x==0):
                    pass
                else:
                    DishTable().delete(self.dish_arr[x-1][0])
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_dish_in_cath()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def add_cath(self):
        """
        Добавление новой категории в таблицу
        """        
        data = []
        data.append(input("Введите название (1 - отмена): ").strip())
        if data[0] == "1":
            return
        while((len(data[0].strip()) == 0)or(len(data[0].strip()) > 32)):
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
    
    def update_cath(self):
        """Функция для обновления категории
        """        
        
        
        
    def show_dish_in_cath(self):
        """Вывод всех блюд в выбранной пользователем категории
        """       
        self.dish_arr = []
        if self.cath_id == -1:
            while True:
                x = int(input('Выберите номер интересуемой категории (0 - отмена): '))
                if(x==0):
                    return
                else:
                    self.cath_id = CathTable().find_by_name(self.cath_arr[x-1])
                    self.cath_obj = self.cath_arr[x-1]
                
                print("Выбрана категория: " + self.cath_obj)
                print("Блюда:")
                print("№\tНазвание\tВремя приготовления\tКраткая инструкция\
                    \n-------------------------------------------------------------------------------------")
                lst = DishTable().all_by_cath_id(self.cath_id)
                
                for i in lst:
                    self.dish_arr.append([i[2], str(i[1]), str(i[4])])
                    
                for i in range(len(self.dish_arr)):
                    print(str(i+1) + "\t" + self.dish_arr[i][0] + "\t\t" + self.dish_arr[i][1] + "\t\t\t" + self.dish_arr[i][2])

                menu = texts.show_dish_in_cath_txt
                print(menu)
                return self.read_next_step()

    def main_cycle(self):
        """Основной цикл программы, регулирующий порядок действий
        """        
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
                
            elif current_menu == "8":
                self.update_cath()
                current_menu = "1"
                
        print("До свидания!")    
        return

        def test(self):
            DbTable.dbconn.test()

m = Main()
# m.test()
m.main_cycle() 