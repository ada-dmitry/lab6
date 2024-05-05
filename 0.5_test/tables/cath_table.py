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
        sql += " WHERE cath_name"
        sql += "=" + "'" + "".join(val) + "';"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
    
    def find_by_name(self, name):
        flag = 0
        cur = self.dbconn.conn.cursor()
        sql_sel = "SELECT id FROM " + self.table_name()
        sql_sel += " WHERE cath_name = " + "'" + name + "'" + ";"
        cur.execute(sql_sel)            
        ret = cur.fetchone()
        # print(ret)
        if(ret != None):
            flag = 1
            return [flag, list(ret)[0]]
        else:
            return [flag, list(ret)[0]]   
        # sql = "SELECT * FROM " + self.table_name()
        # sql += " ORDER BY "
        # sql += ", ".join(self.primary_key())
        # sql += " LIMIT 1 OFFSET %(offset)s"
        # cur.execute(sql, {"offset": num - 1})
        # print(cur)    
    
