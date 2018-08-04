#horsebase = database for storing horses
import sqlite3
import operator
import os
import datetime
import logging

HORSES_TABLE = """CREATE TABLE IF NOT EXISTS horses (
                    id integer PRIMARY KEY,
                    server text NOT NULL,
                    user text NOT NULL,
                    timestamp datetime
                );"""
HORSES_TRIGGER = """CREATE TRIGGER IF NOT EXISTS insert_horses_addtime AFTER INSERT ON horses 
                BEGIN
                UPDATE horses SET timestamp = strftime('%Y-%m-%d %H:%M:%S:%s','now', 'localtime') WHERE id = new.id;
                END"""

def execute(connection, table):
    try:
        c = connection.cursor()
        c.execute(table)
    except Exception as e:
        logging.error(e)

def get_current_count(connection, server, user, after_date=None):
    try:
        c = connection.cursor()
        sql = "SELECT * FROM horses WHERE server=? AND user=?"
        if after_date is not None:
            sql = sql + " AND timestamp > '{}'".format(str(after_date))

        c.execute(sql, (server, user))
        res = c.fetchall()
        if type(res) == list:
            return len(res)
        else:
            return 0
    except Exception as e:
        logging.error(e)

def get_top_count(connection, server, num_results=None, after_date=None):
    try:
        c = connection.cursor()
        sql = "SELECT user, count(*) as c FROM horses WHERE server=?"
        if after_date is not None:
            sql = sql + " AND timestamp >= '{}'".format(str(after_date))
        sql = sql + " GROUP BY user"
        if num_results is not None:
            sql = sql + " LIMIT {}".format(num_results)

        c.execute(sql, (server,))
        res = c.fetchall()
        return res
    except Exception as e:
        logging.error(e)


class HorseBase:
    def __init__(self):
        self.db = sqlite3.connect(os.environ.get('DATABASE_FILE'), isolation_level=None)
        execute(self.db, HORSES_TABLE)
        execute(self.db, HORSES_TRIGGER)

    def add_horse_to_db(self, server, user):
        try:
            c = self.db.cursor()
            c.execute("INSERT INTO horses(server, user) VALUES (?, ?)", (server, user))
        except Exception as e:
            logging.error(e)

    def get_my_horses(self, server, user):
        total = get_current_count(self.db, server, user)
        month = get_current_count(self.db, server, user, datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0))
        return {'total': total, 'month': month}

    def get_top_horses(self, server, num_results):
        all_top = get_top_count(self.db, server, num_results)
        month_top = get_top_count(self.db, server, num_results, datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0))

        return {'alltime': all_top, 'month': month_top}

    def get_total_horses(self, server):
        try:
            c = self.db.cursor()
            c.execute("SELECT count(*) as c FROM horses WHERE server=? GROUP BY server", (server,))
            res = c.fetchone()
            if not res:
                return 0
            else:
                return res[0]
        except Exception as e:
            logging.error(e)