# Таблица с категориями и действия с ними

from dbtable import *
import math

ROW_PER_PAGE = 10

class CathTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "cath"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "cath_name": ["varchar(32)", "NOT NULL"]}

    def table_constraints(self):
        return ['CONSTRAINT "Name" UNIQUE (cath_name)']
    
    def delete(self, id):
        param_sql = f"DELETE FROM cath WHERE id = {id};"
        cur = self.dbconn.conn.cursor()
        cur.execute(param_sql)
        self.dbconn.conn.commit()
    
    def find_by_name(self, name):
        cur = self.dbconn.conn.cursor()
        param_query = "SELECT id FROM cath WHERE cath_name = %s;"
        # sql_sel = "SELECT id FROM " + self.table_name()
        # sql_sel += " WHERE cath_name = " + "'" + name + "'" + ";"
        cur.execute(param_query, (name,))           
        ret = list(cur.fetchone())[0]
        return ret 
    
    def cath_update(self, old):
        """Функция для обновления категории
        """      
        print(f'''Выбрана категория для изменения: {old}''')
        cur = self.dbconn.conn.cursor()

        data = input("Введите название (enter - отмена): ").strip()
        while((len(data.strip()) == 0)or(len(data.strip()) > 32)or(self.check_by_name(data.strip()))):
            if (len(data.strip()) > 32):
                data = input("Название слишком длинное! Введите название заново (enter - отмена):").strip()
            elif(self.check_by_name(data.strip()) == 1):
                data = input("Такое название уже существует. Введите новое (enter - отмена):").strip()
            else:
                return "1"

        param_sql = f"UPDATE cath SET cath_name = '{data}' WHERE cath_name = '{old}';"
        cur.execute(param_sql)
        self.dbconn.conn.commit()
        
    def check_by_name(self, value):
        sql = f"SELECT * FROM {self.table_name()} WHERE cath_name='{value}'" 
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        if result:
            return True
        else:
            return False
        
    def get_cath_page(self, page_num):
        """Функция для получения "страницы" из БД по её номеру.
        В программе заменяет .all() для вывода информации.

        Args:
            page_num (int): номер страницы, определяется пользователем.
        
        Returns: 
            lst (list): Список, содержащий в себе все строки для этой страницы. 
        """        
        final_list = []
        cur = self.dbconn.conn.cursor()
        offset = (page_num - 1) * ROW_PER_PAGE
        sql = (f"SELECT * FROM {self.table_name()} LIMIT {ROW_PER_PAGE} OFFSET {offset}")
        cur.execute(sql)
        zero_list = cur.fetchall()
        for i in range(len(zero_list)):
            final_list.append([str(i+1+(ROW_PER_PAGE*(page_num-1))), str(zero_list[i][0]), zero_list[i][1]])
        return final_list
    
    def get_cath_from_page(self, row_num):
        arr = self.get_cath_page(math.ceil(row_num/ROW_PER_PAGE))
        row = dict()
        for i in arr:
            if(int(i[0]) == row_num):
                row["id"] = str(i[2])
                row["cath_name"] = str(i[1])
        return row 
    # def change_pages(self, )
    
    
    def example_insert(self):
        # self.insert_one(["Завтрак"])
        # self.insert_one(["Обед"])
        # self.insert_one(["Ужин"])
        # self.insert_one(["Перекус"])
        # self.insert_one(["Десерт"])
        # self.insert_one(["Напиток"])
        # self.insert_one(["Закуска"])
        # self.insert_one(["Салат"])
        # self.insert_one(["Гарнир"])
        # self.insert_one(["Выпечка"])
        # self.insert_one(["Супы"])
        # self.insert_one(["Соусы"])
        # self.insert_one(["Паста"])
        # self.insert_one(["Мясные блюда"])
        # self.insert_one(["Рыбные блюда"])
        # self.insert_one(["Веганские блюда"])
        # self.insert_one(["Блюда из птицы"])
        # self.insert_one(["Морепродукты"])
        # self.insert_one(["Национальная кухня"])
        # self.insert_one(["Быстрые блюда"])
        return