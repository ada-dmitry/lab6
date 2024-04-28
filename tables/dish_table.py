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
    
