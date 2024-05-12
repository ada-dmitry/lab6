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
        ret = cur.fetchone()
        return  list(ret)[0] 
        # sql = "SELECT * FROM " + self.table_name()
        # sql += " ORDER BY "
        # sql += ", ".join(self.primary_key())
        # sql += " LIMIT 1 OFFSET %(offset)s"
        # cur.execute(sql, {"offset": num - 1})
        # print(cur)    
    
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