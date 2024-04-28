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
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE " + "".join(self.column_names_without_id())
        sql += "=" + "'" + "".join(val) + "';"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
    
    def find_by_name(self, name):
        cur = self.dbconn.conn.cursor()
        
        sql_sel = "SELECT id FROM " + self.table_name()
        sql_sel += " WHERE cath_name = " + "'" + name + "'" + ";"
        cur.execute(sql_sel) 
        # sql = "SELECT * FROM " + self.table_name()
        # sql += " ORDER BY "
        # sql += ", ".join(self.primary_key())
        # sql += " LIMIT 1 OFFSET %(offset)s"
        # cur.execute(sql, {"offset": num - 1})
        # print(cur)
        return cur.fetchone()       
    
