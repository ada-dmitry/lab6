import sys
import texts
# import time
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
4) UPDATE для категорий - done
5) Красивый вывод - done
6) Доделать ограничение на выбор категории - done
7) UPDATE для блюд - done
8) Постраничный вывод - indev

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
        self.max_cath_index = (len(lst))
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
            if next_step == "4": # Удаление категории
                x = add_func.validate_input('Введите номер удаляемой категории (0 - для отмены): ', 0, self.max_cath_index)
                if(x!=-1):
                    CathTable().delete(self.cath_arr[int(x)-1])
                return "1"
            
            elif next_step == "6": #Добавление блюда в категорию
                DishTable().insert_dishone(self.cath_id)
                next_step = "5"
                
            elif next_step == "7":#Удаление блюда из категории
                x = add_func.validate_input('Введите номер удаляемого блюда (0 - для отмены): ', 0, self.max_index)
                if(x!=-1):
                    DishTable().delete(self.dish_arr[int(x)-1][0])
                else:
                    return "1"     
                next_step = "5"
                
            elif next_step == "5":
                next_step = self.show_dish_in_cath()
                
            elif next_step == "8": # Обновление названия категории
                x = add_func.validate_input('Введите номер обновляемой категории (0 - для отмены): ', 0, self.max_cath_index)
                if(x!=-1):
                    CathTable().cath_update(self.cath_arr[int(x)-1])
                return "1"
            elif next_step == "88":
                x = add_func.validate_input('Введите номер изменяемого блюда (0 - для отмены): ', 0, self.max_index)
                if(x!=-1):
                    DishTable().update_dish(self.dish_arr[int(x)-1][0])
                else:
                    return "1" 
                        
                    
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
        
    def show_dish_in_cath(self):
        """Вывод всех блюд в выбранной пользователем категории
        """       
        self.dish_arr = []
        if self.cath_id == -1:
            while True:
                x = add_func.validate_input('Выберите номер интересуемой категории (0 - отмена): ', 0, self.max_cath_index)
                if(x!=-1):
                    self.cath_id = CathTable().find_by_name(self.cath_arr[x-1])
                    self.cath_obj = self.cath_arr[x-1]
                else:
                    return "1" 
                        
                print("Выбрана категория: " + self.cath_obj)
                print("Блюда:")

                lst = DishTable().all_by_cath_id(self.cath_id)
                self.max_len_name = 0
                self.max_index = len(lst)
                for i in lst:
                    self.dish_arr.append([i[2], str(i[1]), str(i[4])])
                    self.max_len_name = max(self.max_len_name, len(i[2]))
                print("№" + " "*(self.max_index + 1)+ "Название" + " "*(self.max_len_name - 4)\
                    +"Время приготовления     Краткая инструкция\
                        \n-------------------------------------------------------------------------------------------")
                for i in range(len(self.dish_arr)):
                    txt = str(i+1) + " "*(2+self.max_index-len(str(i)))
                    txt += self.dish_arr[i][0] + " "*(4+self.max_len_name - len(self.dish_arr[i][0]))
                    txt += self.dish_arr[i][1] + " "*(5+19-len(self.dish_arr[i][1]))
                    txt += self.dish_arr[i][2]
                    print(txt)
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
                
        print("До свидания!")    
        return

        def test(self):
            DbTable.dbconn.test()

m = Main()
# m.test()
m.main_cycle() 