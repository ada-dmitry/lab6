# Таблица с блюдами и действия с ними

from dbtable import *
import add_func
import math

ROW_PER_PAGE = 10

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
    
#     def get_page_dish(self, cath_id, page_num):
#         offset = (page_num - 1) * ROW_PER_PAGE
#         sql = f"""SELECT * FROM dish WHERE cath_id = {str(cath_id)}\
#  ORDER BY {", ".join(self.primary_key())} LIMIT {ROW_PER_PAGE} OFFSET {offset}"""
#         cur = self.dbconn.conn.cursor()
#         cur.execute(sql)
#         return cur.fetchall()  
        
    def delete(self, id):
        sql = f"""DELETE FROM {self.table_name()} WHERE id = {id};"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
    
    def count(self, id):
        sql = f"""SELECT COUNT(*) FROM {self.table_name()} WHERE cath_id = {id};"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return int(cur.fetchone()[0])
        
    def get_dish_from_page(self, cath_id, row_num):
        arr = self.get_dish_page(cath_id, math.ceil(row_num/ROW_PER_PAGE))
        row = dict()
        for i in arr:
            if(int(i[0]) == row_num):
                row["id"] = i[1]
                row["dish_name"] = str(i[2])
                row["cath_id"] = i[3]
                row["cook_time"] = str(i[4])
                row["manual"] = str(i[5])
        return row 
        
    def get_dish_page(self, cath_id, page_num):
        """Функция для получения "страницы" из БД по её номеру.
        В программе заменяет .all() для вывода информации.

        Args:
            page_num (int): номер страницы, определяется пользователем.
            cath_id (int): id категории, из которой необходимо получить блюда
                    
        Returns: 
            lst (list): Список, содержащий в себе все строки для этой страницы.
             
            0 - number
            1 - id
            2 - name
            3 - cath_id
            4 - cook_time
            5 - manual
        """        
        final_list = []
        cur = self.dbconn.conn.cursor()
        offset = (page_num - 1) * ROW_PER_PAGE
        sql = (f"SELECT * FROM {self.table_name()} WHERE cath_id = {cath_id} LIMIT {ROW_PER_PAGE} OFFSET {offset}")
        cur.execute(sql)
        zero_list = cur.fetchall()
        for i in range(len(zero_list)):
            final_list.append([str(i+1+(ROW_PER_PAGE*(page_num-1))), zero_list[i][3],\
                str(zero_list[i][2]), zero_list[i][0], str(zero_list[i][1]), str(zero_list[i][4])])
        return final_list

        
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
        while True: 
            ins_name = input('Введите название добавляемого блюда (enter - для отмены): ').strip() 
            if(len(ins_name) > 32):
                print("Слишком длинная строка. Повторите ввод!")
            elif(DishTable().check_by_name(ins_name)):
                print('\nТакое блюдо уже существует')
            elif(ins_name == ""):
                return "1"
            else:
                break
        
        ins_time = add_func.input_time_format(ins_name)
            
        ins_manual = input(f'\nПроцесс добавления блюда: {ins_name}\
            \nВведите краткую инструкцию приготовления блюда (enter - для отмены): ').strip()
        if ins_manual == "":
            return "1"
        insert = [cath_id, ins_time, ins_name, ins_manual]
        self.insert_one(insert)
        
    def update_dish(self, obj: dict):
        print('После изменения выберите другой пункт для изменения или введите 0 для выхода')
        x = -10000
        dish_id = obj.get("id")
        dish_name = obj.get("dish_name")
        tmp = dish_name
        while True:
            x = add_func.validate_input(f'\nВыбранное блюдо: {tmp}\nЧто вы хотите изменить в рецепте?\n\
1 - Название\n2 - Время приготовления\n3 - Инструкция\n-1 - для отмены\n=> ', 1, 3)
            
            if(x==1):
                new_name = input(f"Текущее название {tmp}.\nВведите новое название (enter - для отмены): ")
                while (new_name.strip() == '')or(len(new_name.strip()) > 32)\
            or(DishTable().check_by_name(new_name)):
                    if(DishTable().check_by_name(new_name)):
                        print('Такое блюдо уже существует')
                        new_name = input("Повторите ввод! Укажите название блюда (enter - отмена): ")
                        
                    elif(len(new_name.strip()) > 32):
                        new_name = input("Слишком длинная строка. Повторите ввод!\
 Укажите название блюда (enter - отмена): ")
                    else:
                        break
                    
                tmp = new_name
                new_name = "'" + new_name + "'"
                self.update('dish_name', new_name, dish_id)
                    
            elif(x==2):
                new_time = add_func.input_time_format(tmp)
                if(new_time != -1):
                    self.update('cook_time', new_time, dish_id)
                else:
                    break
                
            elif(x==3):
                new_manual = input(f'Введите краткую инструкцию приготовления блюда (enter - для отмены): ')
                if new_manual == "":
                    break
                new_manual = "'" + new_manual + "'"
                self.update('manual', new_manual, dish_id)
            
            elif(x==-1):
                break
        
        
        
        
    def example_insert(self):       
        # self.insert_one([1, "10 minutes", "Яичница", "Взбить яйца, нарезать помидоры, обжарить их вместе."])
        # self.insert_one([1, "20 minutes", "Блины", "Замесить тесто, да пожарить. ©️ Никита Сергеич"])
        # self.insert_one([2, "2 hours", "Хлэб", "Почти, как блины, но не совсем."])
        # self.insert_one([3, "40 minutes", "Паста", "Почувствуй себя итальянцем"])
        # self.insert_one([1, "1 hour", "Пицца", "Раскатать тесто, добавить начинку и запечь в духовке."])
        # self.insert_one([2, "30 minutes", "Салат Цезарь", "Нарезать салат, приготовить соус и обжарить куриную грудку."])
        # self.insert_one([3, "45 minutes", "Лазанья", "Слои теста с соусом и начинкой, запеченные в духовке."])
        # self.insert_one([4, "1 hour 15 minutes", "Жаркое", "Обжарить мясо и овощи, затем потушить в духовке."])
        # self.insert_one([5, "20 minutes", "Смузи", "Смешать фрукты, ягоды, йогурт и лед в блендере."])
        # self.insert_one([6, "2 hours 30 minutes", "Бефстроганов", "Обжарить говядину, приготовить соус и подать с гарниром."])
        # self.insert_one([7, "1 hour", "Чили кон карне", "Обжарить мясо, добавить фасоль, помидоры и специи."])
        # self.insert_one([8, "45 minutes", "Фахитас", "Обжарить мясо и овощи, подать с лепешками и соусом."])
        # self.insert_one([9, "2 hours", "Пельмени", "Приготовить тесто, начинку и слепить пельмени."])
        # self.insert_one([10, "1 hour 30 minutes", "Ризотто", "Обжарить рис, добавить бульон и готовить, постоянно помешивая."])
        # self.insert_one([11, "50 minutes", "Тако", "Обжарить начинку, подать с лепешками и соусами."])
        # self.insert_one([12, "3 hours", "Бараньи ребрышки", "Замариновать ребрышки и запечь в духовке."])
        # self.insert_one([13, "1 hour 15 minutes", "Карри", "Обжарить специи, добавить овощи и курицу, потушить."])
        # self.insert_one([14, "30 minutes", "Бургер", "Обжарить котлету, собрать бургер с соусами и овощами."])
        # self.insert_one([15, "2 hours 45 minutes", "Утка по-пекински", "Замариновать утку, запечь и подать с лепешками и соусом."])
        # self.insert_one([16, "1 hour 30 minutes", "Паэлья", "Обжарить рис с овощами, добавить бульон и морепродукты."])
        # self.insert_one([17, "45 minutes", "Рататуй", "Обжарить овощи и запечь в духовке."])
        # self.insert_one([18, "2 hours", "Борщ", "Обжарить овощи, добавить бульон и тушить."])
        # self.insert_one([19, "1 hour 15 minutes", "Куриные наггетсы", "Замариновать куриное филе, обвалять в панировке и обжарить."])
        # self.insert_one([20, "3 hours", "Индейка с начинкой", "Приготовить начинку, фаршировать индейку и запекать в духовке."])
        # self.insert_one([1, "50 minutes", "Фрикадельки", "Приготовить фарш, сформировать фрикадельки и обжарить."])
        # self.insert_one([2, "2 hours 15 minutes", "Лазанья с мясным соусом", "Приготовить мясной соус, слои теста и запечь в духовке."])
        # self.insert_one([3, "1 hour 30 minutes", "Чили", "Обжарить мясо, добавить фасоль, помидоры и специи, потушить."])
        # self.insert_one([4, "40 minutes", "Хумус", "Приготовить нутовую пасту, добавить специи и подать с питой."])
        # self.insert_one([5, "2 hours 30 minutes", "Утиная ножка по-французски", "Замариновать утиные ножки, обжарить и потушить."])
        # self.insert_one([6, "1 hour 45 minutes", "Лапша по-сингапурски", "Обжарить лапшу с овощами, добавить соус и морепродукты."])
        # self.insert_one([7, "55 minutes", "Фалафель", "Приготовить фалафельную смесь, сформировать шарики и обжарить."])
        # self.insert_one([8, "2 hours 45 minutes", "Жаркое из телятины", "Обжарить мясо, добавить овощи и потушить в духовке."])
        # self.insert_one([9, "1 hour 20 minutes", "Том ям", "Приготовить бульон, добавить морепродукты и специи."])
        # self.insert_one([10, "3 hours 15 minutes", "Баранина по-гречески", "Замариновать баранину, запечь и подать с рисом."])
        # self.insert_one([11, "50 minutes", "Картофельные оладьи", "Приготовить картофельное пюре, сформировать оладьи и обжарить."])
        # self.insert_one([1, "30 minutes", "Омлет", "Взбить яйца, добавить ингредиенты по вкусу и запечь в духовке или обжарить на сковороде."])
        # self.insert_one([1, "25 minutes", "Гренки", "Нарезать хлеб, обжарить на сковороде с маслом и чесноком."])
        # self.insert_one([1, "45 minutes", "Запеканка", "Смешать ингредиенты, выложить в форму и запечь в духовке."])
        # self.insert_one([1, "1 hour", "Ризотто", "Обжарить лук и рис, постепенно добавлять бульон и размешивать."])
        # self.insert_one([1, "20 minutes", "Тосты", "Нарезать хлеб, обжарить на сковороде или в тостере, добавить начинку."])
        # self.insert_one([1, "35 minutes", "Фриттата", "Смесь яиц, овощей и других ингредиентов, запеченная в духовке."])
        # self.insert_one([1, "40 minutes", "Киш", "Открытый пирог с начинкой из яиц, сыра и других ингредиентов."])
        # self.insert_one([1, "1 hour 10 minutes", "Рагу", "Тушеное блюдо из мяса, овощей и специй."])
        # self.insert_one([1, "50 minutes", "Каннеллони", "Трубочки из теста, фаршированные начинкой и запеченные в соусе."])
        # self.insert_one([1, "30 minutes", "Крок-месьё", "Тосты с сыром, запеченные в духовке."])
        # self.insert_one([1, "1 hour 20 minutes", "Мусака", "Слоеное блюдо из баклажанов, мяса и соуса бешамель."])
        # self.insert_one([1, "45 minutes", "Фрикадельки", "Приготовить фарш, сформировать шарики и обжарить или потушить."])
        # self.insert_one([1, "35 minutes", "Зразы", "Фаршированные рулетики из мяса или овощей."])
        # self.insert_one([1, "1 hour", "Чили кон карне", "Острое блюдо из мяса, бобов и специй."])
        # self.insert_one([1, "40 minutes", "Блинчики", "Приготовить тесто, испечь блины и добавить начинку."])
        # self.insert_one([1, "50 minutes", "Кесадилья", "Лепешка с начинкой, запеченная с сыром."])
        # self.insert_one([1, "1 hour 30 minutes", "Паэлья", "Испанское блюдо из риса, морепродуктов и овощей."])
        # self.insert_one([1, "25 minutes", "Сэндвичи", "Хлеб с различными начинками и соусами."])
        # self.insert_one([1, "55 minutes", "Лазанья-роллы", "Рулетики из лазаньи с начинкой и соусом."])
        # self.insert_one([1, "1 hour 10 minutes", "Тефтели", "Фрикадельки в томатном соусе."])
        # self.insert_one([1, "35 minutes", "Вафли", "Приготовить тесто и выпекать в вафельнице."])
        # self.insert_one([1, "45 minutes", "Фахитас", "Мексиканские лепешки с начинкой из мяса, овощей и специй."])
        # self.insert_one([1, "1 hour 20 minutes", "Чили син карне", "Вегетарианская версия чили кон карне."])
        # self.insert_one([1, "30 minutes", "Тартины", "Открытые бутерброды с различными ингредиентами."])
        # self.insert_one([1, "55 minutes", "Энчиладас", "Мексиканские лепешки, завернутые с начинкой и запеченные в соусе."])
        # self.insert_one([1, "1 hour 15 minutes", "Ризотто с морепродуктами", "Ризотто с добавлением креветок, кальмаров и другими морепродуктами."])
        # self.insert_one([1, "40 minutes", "Панини", "Горячие сэндвичи, приготовленные в специальном прессе."])
        # self.insert_one([1, "50 minutes", "Тортилья", "Испанский омлет с картофелем и луком."])
        # self.insert_one([1, "1 hour 30 minutes", "Тажин", "Марокканское блюдо, приготовленное в глиняном горшочке."])
        # self.insert_one([1, "35 minutes", "Брускетта", "Хлеб, обжаренный с чесноком и помидорами."])
        # self.insert_one([1, "1 hour", "Рататуй", "Овощное рагу из баклажанов, цуккини, перца и помидоров."])
        # self.insert_one([1, "45 minutes", "Начос", "Чипсы с начинкой из фасоли, сыра, гуакамоле и сальсы."])
        # self.insert_one([1, "1 hour 20 minutes", "Курица тикка масала", "Индийское блюдо из курицы в пряном соусе."])
        # self.insert_one([1, "30 minutes", "Бутерброды", "Хлеб с различными ингредиентами и соусами."])
        # self.insert_one([1, "55 minutes", "Фалафель", "Жареные шарики из нута с соусами."])
        # self.insert_one([1, "1 hour 15 minutes", "Чана масала", "Индийское блюдо из нута в пряном соусе."])
        # self.insert_one([1, "40 minutes", "Кимчи-боул", "Миска с рисом, кимчи и другими ингредиентами."])
        # self.insert_one([1, "50 minutes", "Такос", "Мексиканские лепешки с начинкой из мяса, овощей и соусов."])
        # self.insert_one([1, "1 hour 30 minutes", "Цуккини-лазанья", "Лазанья с использованием цуккини вместо теста."])
        # self.insert_one([1, "35 minutes", "Брускетта с авокадо", "Хлеб с авокадо, помидорами и специями."])
        # self.insert_one([1, "1 hour", "Чана масала с цветной капустой", "Индийское блюдо из цветной капусты в пряном соусе."])
        # self.insert_one([1, "45 minutes", "Баос", "Мягкие булочки с начинкой из свинины, огурцов и соусов."])
        # self.insert_one([1, "1 hour 20 minutes", "Пад-тай", "Тайская лапша с яйцом, креветками и овощами."])
        # self.insert_one([1, "30 minutes", "Авокадо-тосты", "Тосты с авокадо, яйцом и другими ингредиентами."])
        # self.insert_one([1, "55 minutes", "Кимчи-чигэ", "Острый корейский суп с кимчи и свининой."])
        # self.insert_one([1, "1 hour 15 minutes", "Буррито-боул", "Миска с рисом, фасолью, мясом, овощами и соусами."])
        # self.insert_one([1, "40 minutes", "Баклажаны по-гречески", "Запеченные баклажаны с томатным соусом и сыром."])
        # self.insert_one([1, "50 minutes", "Том-ям", "Острый тайский суп с креветками и грибами."])
        # self.insert_one([1, "1 hour 30 minutes", "Веганский пастуший пирог", "Пастуший пирог с растительными ингредиентами."])
        # self.insert_one([1, "35 minutes", "Сэндвич с авокадо и яйцом", "Бутерброд с авокадо, яйцом и другими ингредиентами."])
        # self.insert_one([1, "1 hour", "Карри с тофу и овощами", "Тайское карри с тофу и смесью овощей."])
        # self.insert_one([1, "45 minutes", "Кимчи-фритата", "Фриттата с добавлением кимчи и других ингредиентов."])
        # self.insert_one([1, "1 hour 20 minutes", "Паста с песто из авокадо", "Паста с соусом из авокадо, базилика и сыра."])
        # self.insert_one([1, "30 minutes", "Яичница с авокадо", "Яичница с добавлением авокадо и других ингредиентов."])
        # self.insert_one([1, "55 minutes", "Веганский пад-тай", "Пад-тай с использованием растительных ингредиентов."])
        return
    