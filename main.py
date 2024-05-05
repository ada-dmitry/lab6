import add_func
import sys
import texts
sys.path.append('tables')

from project_config import *
from dbconnection import *

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
            return next_step;
            
    def show_cath(self):
        self.cath_id = -1
        menu = texts.show_cath_1txt
        print(menu)
        lst = CathTable().all()
        j = 1
        for i in lst:
            print(str(j) + "\t" + str(i[0]))
            j += 1
        menu = texts.show_cath_2txt
        print(menu)
        return
    
    def after_show_cath(self, next_step):
        """Выбор действий после вывода категорий
        """        
        while True:
            if next_step == "4":
                CathTable().delete(input('Введите название удаляемой категории(1 - для отмены): '))
                return "1"
            
            elif next_step == "6": #Добавление блюда в категорию
                DishTable().insert_dishone(self.cath_id)
                next_step = "5"
                
            elif next_step == "7":#Удаление блюда из категории
                del_name = input('Введите название удаляемого блюда (1 - для отмены): ')
                while (del_name.strip() == '')or(len(del_name.strip()) > 32)or(add_func.is_cyr_or_dig(del_name.strip())==0):
                    if(del_name.strip() == ''):
                        del_name = input("Пустая строка. Повторите ввод! Укажите название удаляемого блюда (0 - отмена): ")
                        if del_name == "0":
                            return "1"
                    elif(len(del_name.strip()) > 32):
                        del_name = input("Слишком длинная строка. Повторите ввод!\
                            Укажите название удаляемого блюда (0 - отмена): ")
                        if del_name == "0":
                            return "1"
                    elif(add_func.is_cyr_or_dig(del_name.strip())==0):
                        del_name = input("Название должно состоять только из символов кириллицы. Повторите ввод!\
                            Укажите название удаляемого блюда (0 - отмена): ")
                        if del_name == "0":
                            return "1"
                DishTable().delete(del_name)
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
        while((len(data[0].strip()) == 0)or(len(data[0].strip()) > 32)or(add_func.is_cyr_or_dig(data[0].strip())==0)):
            if (len(data[0].strip()) > 32):
                data[0] = input("Название слишком длинное! Введите название заново (1 - отмена):").strip()
                if data[0] == "1":
                    return
            elif add_func.is_cyr_or_dig(data[0].strip())==0:
                data[0] = input("Название должно состоять только из символов кириллицы!\
                    Введите название заново (1 - отмена):").strip()
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
        if self.cath_id == -1:
            while True:
                name = input("Укажите название категории для вывода блюд (0 - отмена):")
                while (name.strip() == '')or(len(name.strip()) > 32)or(add_func.is_cyr_or_dig(name.strip())==0):
                    if(name.strip() == ''):
                        name = input("Пустая строка. Повторите ввод! Укажите название категории для вывода блюд (0 - отмена):")
                        if name == "0":
                            return "1"
                    elif(len(name.strip()) > 32):
                        name = input("Сликшом длинная строка. Повторите ввод!\
                            Укажите название категории для вывода блюд (0 - отмена):")
                        if name == "0":
                            return "1"
                    elif(add_func.is_cyr_or_dig(name.strip())==0):
                        name = input("Название должно состоять только из символов кириллицы. Повторите ввод!\
                            Укажите название категории для вывода блюд (0 - отмена):")
                        if name == "0":
                            return "1"
                flag, cath = CathTable().find_by_name(name)
                print(flag)
                if flag == 0:
                    print("Введено неверное название!")
                else:
                    self.cath_id = cath
                    # self.cath_obj = cath
                    break
            print("Выбрана категория: " + name)
            print("Блюда:")
            print("№\tНазвание\tВремя приготовления\tКраткая инструкция\
                \n-------------------------------------------------------------------------------------")
            lst = DishTable().all_by_cath_id(cath)
            j = 1
            for i in lst:
                print(str(j) + "\t" + i[2] + "\t\t" + str(i[1]) + "\t\t\t" + str(i[4]))
                j += 1
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
# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
# m.test()
m.main_cycle() 