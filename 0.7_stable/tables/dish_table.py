# Таблица с блюдами и действия с ними

from dbtable import *
import add_func

class DishTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "dish"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "cath_id": ["integer", "REFERENCES cath(id) ON DELETE CASCADE", "NOT NULL"],
                "dish_name": ["varchar(32)", "NOT NULL"],
                "cook_time": ["interval"], 
                "manual": ["text"]}

    def table_constraints(self):
        return ['CONSTRAINT "Name Dish" UNIQUE (dish_name)']



    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()       
    
    def all_by_cath_id(self, cath_id):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE cath_id = " + str(cath_id)
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()  

    def delete(self, val):
        sql = "DELETE FROM dish"
        sql += " WHERE dish_name"
        sql += "=" + "'" + val + "';"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        
    def check_by_name(self, value):
        sql = f"SELECT * FROM {self.table_name()} WHERE dish_name='{value}'" 
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        if result:
            return True
        else:
            return False
    
    def name_by_id(self, id):
        sql = f'SELECT dish_name FROM dish WHERE id = {id}'
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        return str(result)
    
    def id_by_name(self, name):
        sql = f"""SELECT id FROM dish WHERE dish_name = '{name}'"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        return str(result)
    
    def insert_dishone(self, cath_id):
        
        ins_name = input('Введите название добавляемого блюда (1 - для отмены): ')
        
        while (ins_name.strip() == '')or(len(ins_name.strip()) > 32)\
            or(DishTable().check_by_name(ins_name)):
                
            if(ins_name.strip() == ''):
                ins_name = input("Пустая строка. Повторите ввод! Укажите название удаляемого блюда (0 - отмена): ")
                if ins_name == "0":
                    return "1"
                
            elif(len(ins_name.strip()) > 32):
                ins_name = input("Слишком длинная строка. Повторите ввод!\
                    Укажите название удаляемого блюда (0 - отмена): ")
                if ins_name == "0":
                    return "1"
            else:
                print('Такое блюдо уже существует')
                ins_name = input("Повторите ввод! Укажите название блюда (0 - отмена): ")
                if ins_name == "0":
                    return "1"
        
        ins_time = input(f'Процесс добавления блюда: {ins_name}\
            \nВведите время приготовления в формате 10 minutes/1 hour 5 minutes (1 - для отмены): ')
        while(ins_time==0)or(add_func.validate_time_format(ins_time)==False):
            if ins_time == "0":
                return "1"
            else:
                ins_time = input('Время введено в неверном формате. Повторите попытку.\n\
Введите время приготовления в формате 10 minutes/1 hour 5 minutes (1 - для отмены): ')
                
        ins_manual = input(f'Процесс добавления блюда: {ins_name}\
            \nВведите краткую инструкцию приготовления блюда (1 - для отмены): ')
        if ins_manual == "0":
            return "1"
        
        insert = [cath_id, ins_time, ins_name, ins_manual]
        
        self.insert_one(insert)
        
    def update_dish(self, dish):
        print('После изменения выберите другой пункт для изменения или введите 0 для выхода')
        x = -10000
        obj_id = self.id_by_name(dish)[1]
        while(x!=-1):
            x = add_func.validate_input('Что вы хотите изменить в рецепте?\n\
1 - Название\n2 - Время приготовления\n3 - Инструкция\n0 - для отмены\n=> ', 0, 3)
            
            if(x==1):
                new_name = input(f"Текущее название {dish}.\nВведите новое название: ")
                while (new_name.strip() == '')or(len(new_name.strip()) > 32)\
            or(DishTable().check_by_name(new_name)):
                    if(new_name.strip() == ''):
                        new_name = input("Пустая строка. Повторите ввод! Укажите название блюда (0 - отмена): ")
                        if new_name == "0":
                            return "1"
                        
                    elif(len(new_name.strip()) > 32):
                        new_name = input("Слишком длинная строка. Повторите ввод!\
 Укажите название блюда (0 - отмена): ")
                        if new_name == "0":
                            return "1"
                    else:
                        print('Такое блюдо уже существует')
                        new_name = input("Повторите ввод! Укажите название блюда (0 - отмена): ")
                        if new_name == "0":
                            return "1"
                new_name = "'" + new_name + "'"
                self.update('dish_name', new_name, obj_id)
                    
            elif(x==2):
                new_time = input(f'Введите время приготовления в формате 10 minutes/1 hour 5 minutes (1 - для отмены): ')
                while(new_time==0)or(add_func.validate_time_format(new_time)==False):
                    if new_time == "0":
                        return "1"
                    else:
                        new_time = input('Введите время приготовления в формате 10 minutes/1 hour 5 minutes (1 - для отмены): ')
                new_time = "'" + new_time + "'"
                self.update('cook_time', new_time, obj_id)
                
            elif(x==3):
                new_manual = input(f'Введите краткую инструкцию приготовления блюда (1 - для отмены): ')
                if new_manual == "0":
                    return "1"
                new_manual = "'" + new_manual + "'"
                self.update('manual', new_manual, obj_id)
        
        
        
        
    def example_insert(self):       
        self.insert_one([1, "10 minutes", "Яичница", "Взбить яйца, нарезать помидоры, обжарить их вместе."])
        self.insert_one([1, "20 minutes", "Блины", "Замесить тесто, да пожарить. ©️ Никита Сергеич"])
        self.insert_one([2, "2 hours", "Хлэб", "Почти, как блины, но не совсем."])
        self.insert_one([3, "40 minutes", "Паста", "Почувствуй себя итальянцем"])
        self.insert_one([1, "1 hour", "Пицца", "Раскатать тесто, добавить начинку и запечь в духовке."])
        self.insert_one([2, "30 minutes", "Салат Цезарь", "Нарезать салат, приготовить соус и обжарить куриную грудку."])
        self.insert_one([3, "45 minutes", "Лазанья", "Слои теста с соусом и начинкой, запеченные в духовке."])
        self.insert_one([4, "1 hour 15 minutes", "Жаркое", "Обжарить мясо и овощи, затем потушить в духовке."])
        self.insert_one([5, "20 minutes", "Смузи", "Смешать фрукты, ягоды, йогурт и лед в блендере."])
        self.insert_one([6, "2 hours 30 minutes", "Бефстроганов", "Обжарить говядину, приготовить соус и подать с гарниром."])
        self.insert_one([7, "1 hour", "Чили кон карне", "Обжарить мясо, добавить фасоль, помидоры и специи."])
        self.insert_one([8, "45 minutes", "Фахитас", "Обжарить мясо и овощи, подать с лепешками и соусом."])
        self.insert_one([9, "2 hours", "Пельмени", "Приготовить тесто, начинку и слепить пельмени."])
        self.insert_one([10, "1 hour 30 minutes", "Ризотто", "Обжарить рис, добавить бульон и готовить, постоянно помешивая."])
        self.insert_one([11, "50 minutes", "Тако", "Обжарить начинку, подать с лепешками и соусами."])
        self.insert_one([12, "3 hours", "Бараньи ребрышки", "Замариновать ребрышки и запечь в духовке."])
        self.insert_one([13, "1 hour 15 minutes", "Карри", "Обжарить специи, добавить овощи и курицу, потушить."])
        self.insert_one([14, "30 minutes", "Бургер", "Обжарить котлету, собрать бургер с соусами и овощами."])
        self.insert_one([15, "2 hours 45 minutes", "Утка по-пекински", "Замариновать утку, запечь и подать с лепешками и соусом."])
        self.insert_one([16, "1 hour 30 minutes", "Паэлья", "Обжарить рис с овощами, добавить бульон и морепродукты."])
        self.insert_one([17, "45 minutes", "Рататуй", "Обжарить овощи и запечь в духовке."])
        self.insert_one([18, "2 hours", "Борщ", "Обжарить овощи, добавить бульон и тушить."])
        self.insert_one([19, "1 hour 15 minutes", "Куриные наггетсы", "Замариновать куриное филе, обвалять в панировке и обжарить."])
        self.insert_one([20, "3 hours", "Индейка с начинкой", "Приготовить начинку, фаршировать индейку и запекать в духовке."])
        self.insert_one([1, "50 minutes", "Фрикадельки", "Приготовить фарш, сформировать фрикадельки и обжарить."])
        self.insert_one([2, "2 hours 15 minutes", "Лазанья с мясным соусом", "Приготовить мясной соус, слои теста и запечь в духовке."])
        self.insert_one([3, "1 hour 30 minutes", "Чили", "Обжарить мясо, добавить фасоль, помидоры и специи, потушить."])
        self.insert_one([4, "40 minutes", "Хумус", "Приготовить нутовую пасту, добавить специи и подать с питой."])
        self.insert_one([5, "2 hours 30 minutes", "Утиная ножка по-французски", "Замариновать утиные ножки, обжарить и потушить."])
        self.insert_one([6, "1 hour 45 minutes", "Лапша по-сингапурски", "Обжарить лапшу с овощами, добавить соус и морепродукты."])
        self.insert_one([7, "55 minutes", "Фалафель", "Приготовить фалафельную смесь, сформировать шарики и обжарить."])
        self.insert_one([8, "2 hours 45 minutes", "Жаркое из телятины", "Обжарить мясо, добавить овощи и потушить в духовке."])
        self.insert_one([9, "1 hour 20 minutes", "Том ям", "Приготовить бульон, добавить морепродукты и специи."])
        self.insert_one([10, "3 hours 15 minutes", "Баранина по-гречески", "Замариновать баранину, запечь и подать с рисом."])
        self.insert_one([11, "50 minutes", "Картофельные оладьи", "Приготовить картофельное пюре, сформировать оладьи и обжарить."])
        return