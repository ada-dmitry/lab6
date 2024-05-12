from dbtable import *

class CountriesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + '"Сountries"'

    def columns(self):
        return {"country_id": ["serial", "PRIMARY KEY"],
                "name": ["varchar(64)", "NOT NULL", "UNIQUE"]
                }
    def primary_key(self):
        return ["country_id"]
    def column_names_without_id(self):
        res = sorted(self.columns().keys(), key = lambda x: x)
        res.remove('country_id')
        return res
    def find_by_position(self, num):
        sql = f"SELECT * FROM {self.table_name()} ORDER BY name LIMIT 1 OFFSET " + "%(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()       
    def allbyname(self):
        sql = f"SELECT * FROM {self.table_name()} ORDER BY name"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    def findbyname(self, data):
        sql = f"SELECT country_id FROM {self.table_name()} WHERE name = "+ "%s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (data,))
        return cur.fetchall()
    def delete_by_cid(self, cid):
        sql = f"DELETE FROM {self.table_name()} WHERE country_id = " +"%s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (cid,))
        self.dbconn.conn.commit()
        return