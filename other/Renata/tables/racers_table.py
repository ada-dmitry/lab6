# Таблица Телефоны и особые действия с ней.

from dbtable import *

class RacersTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + '"Racers"'

    def columns(self):
        return {"racer_id": ["serial", "PRIMARY KEY"],
                "surname": ["varchar(64)", "NOT NULL"],
                "name": ["varchar(64)", "NOT NULL"],
                "birthday": ["date", "NOT NULL", "CHECK (extract(year from age(current_date, birthday)) < 60)"],
                "country_id": ["integer", "NOT NULL", 'REFERENCES public."Сountries"(country_id) ON DELETE CASCADE'],
                "wins": ["integer", "NOT NULL", "DEFAULT 0"]}
    def table_constraints(self):
        return ["UNIQUE (surname, name, birthday)"]
    def primary_key(self):
        return ["racer_id"]
    def column_names_without_id(self):
        res = sorted(self.columns().keys(), key = lambda x: x)
        res.remove('racer_id')
        return res
    def all_by_country_id(self, cid):
        sql = f"SELECT * FROM {self.table_name()} WHERE country_id = " + "%s ORDER BY surname, name, birthday"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (cid,))
        return cur.fetchall()           
    def delete_by_cid(self, cid):
        sql = f"DELETE FROM {self.table_name()} WHERE country_id = " +"%s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (cid,))
        self.dbconn.conn.commit()
        return
    def find_by_position(self, cid, num):
        sql = f"SELECT * FROM {self.table_name()} WHERE "+ "country_id = %(cid)s ORDER BY surname, name, birthday LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"cid": cid, "offset": num - 1})
        return cur.fetchone()
    def delete_by_rid(self, rid):
        sql = f"DELETE FROM {self.table_name()} WHERE racer_id = " +"%s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (rid,))
        self.dbconn.conn.commit()
        return
    def checkbirthday(self, val):
        sql = "SELECT extract(year from age(current_date, %s)) >= 60"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (val,))
        return cur.fetchone()
    def select_by_s_n_b(self, vals):
        sql = f"SELECT racer_id FROM {self.table_name()} WHERE name = " + "%s AND surname = %s AND birthday = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, vals)
        return cur.fetchone()
    def insertbydef(self, vals):
        sql = f"INSERT INTO {self.table_name()}(birthday, country_id, name, surname) VALUES "+"(%s,%s,%s,%s)"
        cur = self.dbconn.conn.cursor()
        print(vals)
        cur.execute(sql, vals)
        self.dbconn.conn.commit()
        return