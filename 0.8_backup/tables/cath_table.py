# Таблица с категориями и действия с ними

from dbtable import *

class CathTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "cath"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "cath_name": ["varchar(32)", "NOT NULL"]}

    def table_constraints(self):
        return ['CONSTRAINT "Name" UNIQUE (cath_name)']
    
    def delete(self, val):
        param_sql = "DELETE FROM cath WHERE cath_name = %s;"
        cur = self.dbconn.conn.cursor()
        value = "".join(val)
        cur.execute(param_sql, (value,))
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

        data = input("Введите название (1 - отмена): ").strip()
        if data == "1":
            return
        while((len(data.strip()) == 0)or(len(data.strip()) > 32)or(self.check_by_name(data.strip()))):
            if (len(data.strip()) > 32):
                data = input("Название слишком длинное! Введите название заново (1 - отмена):").strip()
                if data == "1":
                    return
            elif len(data.strip()) == 0:
                data = input("Название не может быть пустым! Введите название заново (1 - отмена):").strip()
                if data == "1":
                    return
            else:
                data = input("Такое название уже существует. Введите новое (1 - отмена):").strip()

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
    
    
    def example_insert(self):
        self.insert_one(["Завтрак"])
        self.insert_one(["Обед"])
        self.insert_one(["Ужин"])
        self.insert_one(["Перекус"])
        self.insert_one(["Десерт"])
        self.insert_one(["Напиток"])
        self.insert_one(["Закуска"])
        self.insert_one(["Салат"])
        self.insert_one(["Гарнир"])
        self.insert_one(["Выпечка"])
        self.insert_one(["Супы"])
        self.insert_one(["Соусы"])
        self.insert_one(["Паста"])
        self.insert_one(["Мясные блюда"])
        self.insert_one(["Рыбные блюда"])
        self.insert_one(["Веганские блюда"])
        self.insert_one(["Блюда из птицы"])
        self.insert_one(["Морепродукты"])
        self.insert_one(["Национальная кухня"])
        self.insert_one(["Быстрые блюда"])
        return