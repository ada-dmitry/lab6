import sys
import math

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
7) UPDATE для блюд - done 0.7
8) Постраничный вывод - indev 0.8 - реализация через offset.
9) Реализовать отдельный просмотр(offset) - done for cath
10) И отдельный вывод(offset)


1) detele category - done
2) update category - done
3) add category - done

FIXME:
1) Откомментировать os.cls
2) Исправить вылет при неверном вводе в самое начало(сделать выход на предыдущую менюшку)
3) При вводе текста пропуск сделать с помощью пустой строки.

TEST:
1) Удаление категории + ввод неизвестных символов и отмена
2) Обновление категории + ввод неизвестных символов и отмена
3) Добавление категории + ввод неизвестных символов и отмена

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
        
    def show_page_cath(self):
        menu = """Просмотр списка категорий!
№\tНазвание\n-------------------------------------------------------------------------------------------"""
        
        cath_page = 1
        lst = CathTable().get_cath_page(cath_page)
        action = '>'
        max_page = math.ceil(self.max_cath_index/10)
        while True:
            cath_arr = CathTable().get_cath_page(cath_page)
            add_func.cls()
            print(menu)
            
            for i in range(len(cath_arr)):
                print(add_func.add_zero_before(cath_arr[i][0],\
                    len(str(self.max_cath_index))) + "\t" + cath_arr[i][1])
                
            action = input('-------------------------------------------------------------------------------------------\n\
Для переключения между страницами используйте "<" и ">"\nКол-во записей на странице: 10\n\
Для выхода в меню действий нажмите любую другую клавишу\n=> ')
            
            if(action=='>'):
                if(cath_page==max_page):
                    cath_page = 1
                else:
                    cath_page += 1
                lst = CathTable().get_cath_page(cath_page)
            elif(action=='<'):
                if(cath_page==1):
                    cath_page = max_page
                else:
                    cath_page -= 1
                lst = CathTable().get_cath_page(cath_page)
            else:
                break
        
        
            
    def show_cath(self):
        self.cath_id = -1
        self.max_cath_index = CathTable().count()
        self.show_page_cath()
        menu = """-------------------------------------------------------------------------------------------\nДальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление новой категории;
    4 - удаление категории;
    5 - просмотр блюд в категории;
    8 - обновить категорию;
    9 - выход."""
        print(menu)
        return
    
    def after_show_cath(self, next_step):
        """Выбор действий после вывода категорий
        """
        while True:
            if next_step == "4": # Удаление категории
                left = 0
                right = self.max_cath_index
                x = add_func.validate_input('Введите номер удаляемой категории (0 - для отмены): ', left, right)
                if(x!=-1):
                    CathTable().delete(CathTable().get_cath_from_page(x).get("id"))
                return "1"
            
            elif next_step == "6": #Добавление блюда в категорию
                DishTable().insert_dishone(self.cath_id)
                next_step = "5"
                
            elif next_step == "7":#Удаление блюда из категории
                left = 0
                right = self.max_dish_index
                x = add_func.validate_input('Введите номер удаляемого блюда (0 - для отмены): ', left, right)
                if(x!=-1):
                    DishTable().delete(DishTable().get_dish_from_page(x).get("id"))
                else:
                    return "1"     
                next_step = "5"
                
            elif next_step == "5":
                next_step = self.show_dish_in_cath()
                
            elif next_step == "8": # Обновление названия категории
                left = 0
                right = self.max_cath_index
                x = add_func.validate_input('Введите номер обновляемой категории (0 - для отмены): ', left, right)
                if(x!=-1):
                    CathTable().cath_update(CathTable().get_cath_from_page(x).get("cath_name"))
                return "1"
            
            elif next_step == "88": # Обновление блюда
                left = 0
                right = self.max_dish_index
                x = add_func.validate_input('Введите номер обновляемого блюда (0 - для отмены): ', left, right)
                if(x!=-1):
                    DishTable().update_dish(DishTable().get_dish_from_page(x))
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
        data = input("Введите название (enter - отмена): ").strip()
        while((len(data) == 0)or(len(data) > 32)or(CathTable().check_by_name(data))):
            if (len(data) > 32):
                data = input("Название слишком длинное! Введите название заново (enter - отмена): ").strip()
            elif(CathTable().check_by_name(data)):
                data = input("Такое название уже существует! Введите название заново (enter - отмена): ").strip()
            else:
                return
        CathTable().insert_one(data)
        return
    
    def show_dish_page(self):
            print("Блюда:")
            dish_page = 1
            lst = DishTable().get_dish_page(self.cath_id, dish_page)
            self.max_len_name = 0
            self.max_dish_index = DishTable().count(self.cath_id)
            action = '>'
            max_page = math.ceil(self.max_dish_index/10)
            lst = DishTable().get_dish_page(self.cath_id, dish_page)
            
            while True:
                self.dish_arr = []
                
                for i in lst:
                    self.dish_arr.append([i[2], str(i[1]), str(i[4])])
                    self.max_len_name = max(self.max_len_name, len(i[2]))
                add_func.cls()
                print("№" + " "*(len(str(self.max_dish_index)) + 1)+ "Название" + " "*(self.max_len_name - 4)\
                    +"Время приготовления     Краткая инструкция\
                        \n-------------------------------------------------------------------------------------------")
                
                for i in range(len(self.dish_arr)):
                    txt = add_func.add_zero_before(str((i+1)+(10*(dish_page-1))), \
                        len(str(self.max_dish_index))) + " "*(2+len(str(self.max_dish_index)))
                    txt += self.dish_arr[i][0] + " "*(4+self.max_len_name - len(self.dish_arr[i][0]))
                    txt += self.dish_arr[i][1] + " "*(5+19-len(self.dish_arr[i][1]))
                    txt += self.dish_arr[i][2]
                    print(txt)
                action = input('-------------------------------------------------------------------------------------------\n\
    Для переключения между страницами используйте "<" и ">"\nКол-во записей на странице: 10\n\
    Для выхода в меню действий нажмите любую другую клавишу\n=> ')
                if(action=='>'):
                    if(dish_page==max_page):
                        dish_page = 1
                    else:
                        dish_page += 1
                    lst = DishTable().get_dish_page(self.cath_id, dish_page)
                elif(action=='<'):
                    if(dish_page==1):
                        dish_page = max_page
                    else:
                        dish_page -= 1
                    lst = DishTable().get_dish_page(self.cath_id, dish_page)
                else:
                    break
        
    def show_dish_in_cath(self):
        """Вывод всех блюд в выбранной пользователем категории
        """       
        if self.cath_id == -1:
            while True:
                left = 0
                right = self.max_cath_index
                x = add_func.validate_input('Выберите номер интересуемой категории (0 - отмена): ', left, right)
                add_func.cls()
                if(x!=-1):
                    self.cath = CathTable().get_cath_from_page(x)
                    self.cath_obj = self.cath.get("cath_name")
                    self.cath_id = self.cath.get("id")
                else:
                    return "1" 
                self.show_dish_page()
                print(f"Выбрана категория: {self.cath_obj}")
                
                    
                menu = """-------------------------------------------------------------------------------------------\nДальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр категорий;
    6 - добавление нового блюда;
    7 - удаление блюда;
    88 - для обновления блюда;
    9 - выход."""
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