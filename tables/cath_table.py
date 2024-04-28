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
    
    
    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()       
    
