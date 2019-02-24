# coding: utf-8
#!/usr/bin/env python
from math import sin, cos, sqrt, atan2, radians
import sqlite3 as sqlite
import os
from pypika import Query, Table, Field
import time

class db(object):
    def __init__(self):
        self.file_route = os.path.dirname(os.path.abspath(__file__))

    def connAndClose(db):
        """
        Use @connAndClose(db={db name}), you can open db
        example:
        @connAndClose(db={db name})
        def fuc(slef, c):
            c.execute(something)
        """
        def decorator(func):
            def decorator(self, *args, **kwargs):
                conn = sqlite.connect("{}/../res/{}".format(self.file_route, db))
                c = conn.cursor()
                ret = func(self, c, *args, **kwargs)
                conn.commit()
                conn.close()
                return ret
            return decorator
        return decorator

    def checkExistsQuery(self, query):
        return "SELECT EXISTS({})".format(str(query))

    def selectStatusQuery(self, user_id, select_content):
        status = Table("status")
        return str(Query\
            .from_(status)\
            .select(select_content)\
            .where(status.user_id == user_id))

    @connAndClose(db="users.db")
    def insertDiscuss(self, c, user_id, word_content=None, timestamp=None):
        if timestamp == None :timestamp = time.time()
        c.execute(
            self.insertDiscussQuery(user_id, word_content, timestamp)
        )

    def insertDiscussQuery(self, user_id, word_content=None, timestamp=None):
        discuss = Table("discuss")
        return str(Query.into(discuss)\
            .columns("user_id", "timestamp", "word")\
            .insert(user_id, timestamp, word_content))

    @connAndClose(db="users.db")
    def updateLastDiscuss(self, c, user_id, set_content, value):
        c.execute(
            self.updateLastDiscussQuery(user_id, set_content, value)
        )

    def updateLastDiscussQuery(self, user_id, set_content, value):
        discuss = Table("discuss")
        last_timestampQuery = str(Query\
            .from_(discuss)\
            .select("timestamp")\
            .where(discuss.user_id == user_id))
        last_timestampQuery = str(last_timestampQuery).replace('"timestamp"', 'MAX("timestamp")')
        return str(Query\
            .update(discuss)\
            .set(set_content, value)\
            .where(discuss.user_id == user_id)) + ' AND "timestamp"=({})'.format(last_timestampQuery)

    @connAndClose(db="users.db")
    def updateStatus(self, c, user_id, action):
        print("update user action : {}".format(action))
        c.execute(self.updateStatusQuery(user_id, action))

    def updateStatusQuery(self, user_id, action):
        status = Table("status")
        return str(Query\
            .update(status)\
            .set('action', action)\
            .where(status.user_id == user_id))

    @connAndClose(db="users.db")
    def selectStatus(self, c, user_id, action="default"):
        if bool(c.execute(self.checkExistsQuery(self.selectStatusQuery(user_id, "user_id"))).fetchall()[0][0]):
            action = c.execute(self.selectStatusQuery(user_id, "action")).fetchall()[0][0]
            print("select user action : {}".format(action))
            return action
        else:
            print("inser user action : default")
            c.execute(self.insertStatusQuery(user_id, action))
            return "default"

    def insertStatusQuery(self, user_id, action):
        status = Table("status")
        return str(Query.into(status)\
            .columns("user_id", "action")\
            .insert(user_id, action))