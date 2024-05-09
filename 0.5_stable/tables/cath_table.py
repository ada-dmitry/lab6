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
        # sql = "DELETE FROM " + self.table_name()
        # sql += " WHERE cath_name"
        # sql += "=" + "'" + "".join(val) + "';"
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
        return