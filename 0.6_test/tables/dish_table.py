# Таблица с блюдами и действия с ними

from dbtable import *

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
        if ins_time == "0":
            return "1"
        ins_manual = input(f'Процесс добавления блюда: {ins_name}\
            \nВведите краткую инструкцию приготовления блюда (1 - для отмены): ')
        if ins_time == "0":
            return "1"
        
        insert = [cath_id, ins_time, ins_name, ins_manual]
        DishTable().insert_one(insert)
        
        
    def example_insert(self):       
        self.insert_one([1, "10 minutes", "Яичница", "Взбить яйца, нарезать помидоры, обжарить их вместе."])
        self.insert_one([1, "20 minutes", "Блины", "Замесить тесто, да пожарить. ©️ Никита Сергеич"])
        self.insert_one([2, "2 hours", "Хлэб", "Почти, как блины, но не совсем."])
        self.insert_one([3, "40 minutes", "Паста", "Почувствуй себя итальянцем"])
        return