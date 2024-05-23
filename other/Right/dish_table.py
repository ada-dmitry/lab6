from dbtable import *

class DishTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Dish"

    def exist_by_number(self, dish_id):
        sql = f"SELECT COUNT(*) FROM {self.table_name()} WHERE dish_id = %(id)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {'id': str(dish_id)})
        return cur.fetchone()[0] > 0

    def columns(self):
        return {"dish_id": ["serial", "PRIMARY KEY"],
                "name": ["varchar(64)", "NOT NULL"],
                "cook_time": ["integer", "NOT NULL"],
                "manual": ["text", "NOT NULL"],
                "cath_id": ["integer", "NOT NULL"]}

    def primary_key(self):
        return ["dish_id"]

    def get_all_by_cathegory_number(self, cathegory_number):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE cath_id = %(id)s"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        print(str(cathegory_number))
        cur.execute(sql, {'id': str(cathegory_number)})
        return cur.fetchall()

    def delete_one(self, data):
        if type(data)==int:
            sql = f"DELETE FROM {self.table_name()} WHERE dish_id = %(id)s"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, {'id': str(data)})
            self.dbconn.conn.commit()
        elif type(data)==str:
            sql = f"DELETE FROM {self.table_name()} WHERE name = %(name)s"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, {'name': str(data)})
            self.dbconn.conn.commit()
        return

    def delete_all_with_cathegory_id(self, cathegory_id):
        sql = f"DELETE FROM {self.table_name()} WHERE cath_id = %(id)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {'id': str(cathegory_id)})
        self.dbconn.conn.commit()


    
