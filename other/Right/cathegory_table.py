# Таблица Телефоны и особые действия с ней.

from dbtable import *
import re

class CathegoryTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Cathegory"

    def columns(self):
        return {"cath_id": ["serial", "PRIMARY KEY"],
                "cath_name": ["varchar(20)", "NOT NULL"]}

    def primary_key(self):
        return ["cath_id"]

    def delete_one(self, data):
        if type(data)==int:
            sql = f"DELETE FROM {self.table_name()} WHERE cath_id = %(id)s"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, {'id': str(data)})
            self.dbconn.conn.commit()
        elif type(data)==str:
            sql = f"DELETE FROM {self.table_name()} WHERE name = %(name)s"
            cur = self.dbconn.conn.cursor()
            
            cur.execute(sql, {'name': str(data)})
            self.dbconn.conn.commit()
        return

    def exist_by_number(self, data):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE cath_id = %(id)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {'id': str(data)})
        return len(cur.fetchall()) > 0


    def update(self, cathegory_id, data):
        sql = "UPDATE " + self.table_name()
        sql += " SET cath_name = '" + re.split(r"'|--|\(|\)", data[0])[0] + "'"
        sql += " WHERE cath_id = %(id)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {'id': str(cathegory_id)})
        self.dbconn.conn.commit()