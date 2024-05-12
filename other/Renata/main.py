import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.countries_table import *
from tables.racers_table import *
from extra_functions import * 
class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        ct = CountriesTable()
        rt = RacersTable()
        ct.create()
        rt.create()
        return

    def db_insert_somethings(self):
        ct = CountriesTable()
        rt = RacersTable()
        ct.insert_one(["Germany"])
        ct.insert_one(["United Kingdom"])
        ct.insert_one(["Netherlands"])
        ct.insert_one(["Finland"])
        ct.insert_one(["Mexico"])
        ct.insert_one(["Switzerland"])
        rt.insert_one(['1985-01-07', 1,'Lewis', 'Hamilton', 100])
        rt.insert_one(['1997-09-30', 3,'Max', 'Verstappen', 50])
        rt.insert_one(['1989-08-28', 4,'Valtteri', 'Bottas', 30])
        rt.insert_one(['1989-07-01', 1,'Daniel', 'Ricciardo', 15])
        rt.insert_one(['1990-01-26', 5,'Sergio', 'Perez', 10])

    def db_drop(self):
        ct = CountriesTable()
        rt = RacersTable()
        rt.drop()
        ct.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр стран;
    2 - сброс и инициализация таблиц;
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
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step
            
    def show_countries(self):
        self.country_id = -1
        menu = """Просмотр списка стран!
№\tНазвание страны"""
        print(menu)
        lst = CountriesTable().allbyname()
        for index, i in enumerate(lst):
            print(str(index+1) + "\t" + i[1])
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление новой страны;
    4 - удаление страны;
    5 - просмотр гонщиков, родившихся в этой стране;
    9 - выход."""
        print(menu)
        return

    def after_show_countries(self, next_step):
        while True:
            if next_step == "4":
                self.delete_country()
                return "1"
            elif next_step == "5":
                next_step = self.after_show_racers(self.show_racers_by_countries())
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step
    def after_show_racers(self, next_step):
        while True:
            if next_step == "3":
                self.insert_new_racer()
            elif next_step == "4":
                self.delete_racer()
            elif next_step == "0" or next_step == "9" or next_step == "1":
                return next_step
            else:
                print('Ввели неверное число')
            return "5"
            
    def delete_country(self):
        num = input("Введите номер строки, в которой находится страна, которую вы хотите удалить (0 - отмена): ").strip()
        if num == "0":
            return
        while len(num) == 0 or not(num.isdigit()) or not(CountriesTable().find_by_position(int(num))):
            if len(num) == 0:
                text = "Номер строки не пустое значение!"
            elif not(num.isdigit()):
                text = "Номер строки это положительное ЧИСЛО!"
            else:
                text = "Номер строки вне диапазона!"
            num = input(text + " Введите номер строки снова (0 - отмена): ").strip()
            if num == "0":
                return
        self.country_id = int(CountriesTable().find_by_position(int(num))[0])
        RacersTable().delete_by_cid(self.country_id)
        CountriesTable().delete_by_cid(self.country_id)
    def show_add_country(self):
        data = input("Введите название страны (-1 - отмена): ").strip()
        if data == "-1":
            return
        while len(data) == 0 or len(data) > 64 or CountriesTable().findbyname(data):
            if len(data) == 0:
                text = "Название страны не пустое!"
            elif len(data) > 64:
                text = "Название страны не превышает 64 значения!"
            else:
                text = "Такая страна уже есть в таблице!"
            data = input(text + " Введите название страны снова (-1 - отмена): ").strip()
            if data == "-1":
                return
        CountriesTable().insert_one([data])

    def show_racers_by_countries(self):
        if self.country_id == -1:
            num = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена): ").strip()
            while len(num) == 0 or not(num.isdigit()) or not(CountriesTable().find_by_position(int(num))):
                if len(num) == 0:
                    text = "Номер строки не пустое значение!"
                elif not(num.isdigit()):
                    text = "Номер строки это положительное ЧИСЛО!"
                else:
                    text = "Номер строки вне диапазона!"
                num = input(text + " Введите номер строки снова (0 - отмена): ").strip()
                if num == "0":
                    return
            country = CountriesTable().find_by_position(int(num))
            self.country_id = int(country[0])
            self.country_name = country[1]        
        print("Выбрана страна: " + self.country_name)
        print("Гонщики:")
        lst = RacersTable().all_by_country_id(self.country_id)
        self.rac_max_len = len(str(len(lst)))
        self.max_sur_len = max_len(lst, 4)
        self.max_name_len = max_len(lst, 2)
        menu = "№" + " "*(self.rac_max_len + 1)+ "Фамилия" + " "*(self.max_sur_len - 5)  +"Имя" + " "*(self.max_name_len - 1) +"День рождения  Количество побед" 
        print(menu)
        for index, i in enumerate(lst):
            text = str(index+1) + " "*(self.rac_max_len-len(str(index+1))+2)+i[4]+ \
                " "*(self.max_sur_len-len(i[4])+2)+i[2]+ " "*(self.max_name_len-len(i[2])+2)
            text += str(i[0]) + " "*5+str(i[5])
            print(text)
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр стран;
    3 - добавление нового гонщика;
    4 - удаление гонщика;
    9 - выход."""
        print(menu)
        return self.read_next_step()

    def insert_new_racer(self):
        while True:
            data = []
            data.append(input("Введите имя гонщика (-1 - отмена): ").strip())
            if data[0] == "-1":
                return
            while len(data[0]) == 0 or len(data[0]) > 64:
                if len(data[0]) == 0:
                    text = 'Имя не может быть пустым!'
                else:
                    text = 'Имя превышает 64 символа!'
                data[0] = input(text + " Введите имя заново (-1 - отмена): ").strip()
                if data[0] == "-1":
                    return
            data.append(input("Введите фамилию гонщика (-1 - отмена): ").strip())
            if data[1] == "-1":
                return
            while len(data[1]) == 0 or len(data[1]) > 64:
                if len(data[1]) == 0:
                    text = 'Фамилия не может быть пустым!'
                else:
                    text = 'Фамилия не превышает 64 символа!'
                data[1] = input(text + " Введите фамилию заново (-1 - отмена): ").strip()
                if data[1] == "-1":
                    return
            data.append(input("Введите день рождения гонщика в формате (ГГГГ-ММ-ДД)(1976-04-03 - 3 апреля 1976 года), причем гонщику должно быть меньше 60 лет (-1 - отмена): ").strip())
            if data[2] == "-1":
                return
            while len(data[2]) == 0 or check_format(data[2]) or RacersTable().checkbirthday(data[2])[0]:
                if len(data[2]) == 0:
                    text = 'День рождения не может быть пустым!'
                elif check_format(data[2]):
                    text = 'Строка не соответствует формату дня рождения!'
                else:
                    text = 'Гонщику больше 60 лет!'
                data[2] = input(text + " Введите день рождения гонщика заново (ГГГГ-ММ-ДД) (-1 - отмена): ").strip()
                if data[2] == "-1":
                    return
            self.racer = RacersTable().select_by_s_n_b(data)
            if not(self.racer):
                break
            print('Такой гонщик уже есть!', end = ' ')
        data.append(self.country_id)
        data[2], data[0], data[1], data[3] = data[0], data[2], data[3], data[1]
        data.append(input("Введите количество побед гонщика (пробелы - значение по умолчанию: 0)(-1 - отмена): ").strip())
        if data[4] == "-1":
            return
        if len(data[4]) == 0:
            RacersTable().insertbydef(data[:-1])
            return
        while not(data[4].isdigit()):
            text = "Количество побед это Положительное ЧИСЛО!"
            data[4] = input(text + " Введите количество побед снова (-1 - отмена): ").strip()
            if data[4]== "-1":
                return
        RacersTable().insert_one(data)
        
    def delete_racer(self):
        num = input("Введите номер строки, в которой находится гонщик, которого вы хотите удалить (0 - отмена): ").strip()
        if num == "0":
            return
        while len(num) == 0 or not(num.isdigit()) or not(RacersTable().find_by_position(self.country_id, int(num))):
            if len(num) == 0:
                text = "Номер строки не пустое значение!"
            elif not(num.isdigit()):
                text = "Номер строки это положительное ЧИСЛО!"
            else:
                text = "Номер строки вне диапазона!"
            num = input(text + " Введите номер строки снова (0 - отмена): ").strip()
            if num == "0":
                return
        RacersTable().delete_by_rid(int(RacersTable().find_by_position(self.country_id, int(num))[3]))
    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_countries()
                next_step = self.read_next_step()
                current_menu = self.after_show_countries(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_country()
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
    
