import sqlite3 as db
import glob, json

class DB:

    def __init__(self):
        self.conn = db.connect('countdown.db')
        self.cursor = self.conn.cursor()

    def add_data(self, data):
        query = 'INSERT INTO countdown (title, date) VALUES (?, ?)'
        self.cursor.execute(query, (data['title'], data['date']))
        self.conn.commit()

    def countdown_row_mapper(self, res):
        res_list = []
        for row in res:
            res_list.append({
                "id": row[0],
                "title": row[1],
                "date": row[2]
            })
        return {
            "events" : res_list
        }

    def get_all(self):
        query = "SELECT * FROM countdown"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return self.countdown_row_mapper(res)

    def print_all_data(self):
        query = "SELECT * FROM countdown"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        restr = ''
        for r in res:
            restr = restr + '<br><br>' + r[1] + ' ' + r[2] + '<br>' 
            print(r)
        return restr

    def delete(self, cid):
        query = "DELETE FROM countdown WHERE id = ?"
        print(cid)
        self.cursor.execute(query, (cid, ))
        res = self.conn.commit()

# dbs = DB()
# dbs.add_from_images_folder()
# print dbs.print_all_data()