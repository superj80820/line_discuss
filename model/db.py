# coding: utf-8
#!/usr/bin/env python
from math import sin, cos, sqrt, atan2, radians
import sqlite3 as sqlite
import os
from pypika import Query, Table, Field
import time
import json

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

    def selectStatusQuery(self, select_content, where_content, where_value):
        status = Table("status")
        return str(Query\
            .from_(status)\
            .select(select_content)\
            .where(getattr(status, where_content) == where_value))

    def selectRoomQuery(self, room_id, select_content):
        room = Table("room")
        return str(Query\
            .from_(room)\
            .select(select_content)\
            .where(room.room_id == room_id))

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
    def selectDiscuss(self, c):
        return c.execute(
            self.selectDiscussQuery()
        ).fetchall()[0]

    def selectDiscussQuery(self):
        discuss = Table("discuss")
        return str(Query\
            .from_(discuss)\
            .select("image")\
            .select("word"))

    @connAndClose(db="users.db")
    def updateStatus(self, c, set_content, set_value, select_content, select_value):
        print("update user status : {}".format(set_content))
        c.execute(self.updateStatusQuery(set_content, set_value, select_content, select_value))

    def updateStatusQuery(self, set_content, set_value, select_content, select_value):
        status = Table("status")
        return str(Query\
            .update(status)\
            .set(set_content, set_value)\
            .where(getattr(status, select_content) == select_value))

    @connAndClose(db="users.db")
    def selectStatusAction(self, c, user_id, action="default"):
        if bool(c.execute(self.checkExistsQuery(self.selectStatusQuery("user_id", "user_id", user_id))).fetchall()[0][0]):
            action = c.execute(self.selectStatusQuery("action", "user_id", user_id)).fetchall()[0][0]
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

    @connAndClose(db="users.db")
    def selectStatus(self, c, select_content, where_content, where_value):
        return c.execute(self.selectStatusQuery(select_content, where_content, where_value)).fetchall()

    @connAndClose(db="users.db")
    def selectStatusRoomIdMembers(self, c, room_id):
        ret = c.execute(self.selectStatusRoomIdMembersQuery(room_id)).fetchall()
        ret = {"members": list(map(lambda x:x[1], ret)), "count": len(ret)}
        return ret

    def selectStatusRoomIdMembersQuery(self, room_id):
        status = Table("status")
        return str(Query\
            .from_(status)\
            .select("room_id")\
            .select("name")\
            .where(status.room_id == room_id)\
            .where(status.arrive == "true"))

    @connAndClose(db="users.db")
    def insertRoom(self, c, inser_content, room_id):
        if bool(c.execute(self.checkExistsQuery(self.selectRoomQuery(room_id, "room_id"))).fetchall()[0][0]):
            print("room is exist")
            return False
        else:
            print("insert room, {}: {}".format(inser_content, room_id))
            c.execute(self.insertRoomQuery(inser_content, room_id))
            return True

    def insertRoomQuery(self, inser_content, value):
        room = Table("room")
        return str(Query.into(room)\
            .columns(inser_content)\
            .insert(value))

    @connAndClose(db="users.db")
    def updateRoom(self, c, set_content, set_value, select_content, select_value):
        print("update user room : {}".format(set_content))
        c.execute(self.updateRoomQuery(set_content, set_value, select_content, select_value))

    def updateRoomQuery(self, set_content, set_value, select_content, select_value):
        room = Table("room")
        return str(Query\
            .update(room)\
            .set(set_content, set_value)\
            .where(getattr(room, select_content) == select_value))

    @connAndClose(db="users.db")
    def selectRoom(self, c, room_id, select_content):
        return int(c.execute(self.selectRoomQuery(room_id, select_content)).fetchall()[0][0])

    @connAndClose(db="users.db")
    def insertVote(self, c, room_id, vote_id, vote_data):
        print("insert vote, room_id: {}".format(room_id))
        timestamp = time.time()
        vote_data = json.dumps(vote_data)
        c.execute(self.insertVoteQuery(room_id, vote_id, vote_data, timestamp))

    def insertVoteQuery(self, room_id, vote_id, vote_data, timestamp):
        vote = Table("vote")
        return str(Query.into(vote)\
            .columns("room_id", "vote_id", "vote_data", "timestamp")\
            .insert(room_id, vote_id, vote_data, timestamp))

    @connAndClose(db="users.db")
    def updateVote(self, c, set_content, set_value, select_content, select_value):
        if set_content == "vote_data":
            set_value = json.dumps(set_value)
        else:
            set_value = str(set_value)
        print("update vote, {}: {}".format(set_content, set_value))
        c.execute(self.updateVoteQuery(set_content, set_value, select_content, select_value))

    def updateVoteQuery(self, set_content, set_value, select_content, select_value):
        vote = Table("vote")
        return str(Query\
            .update(vote)\
            .set(set_content, set_value)\
            .where(getattr(vote, select_content) == select_value))

    @connAndClose(db="users.db")
    def selectVote(self, c, vote_id, select_content):
        return json.loads(c.execute(self.selectVoteQuery(vote_id, select_content)).fetchall()[0][0])

    def selectVoteQuery(self, vote_id, select_content):
        vote = Table("vote")
        return str(Query\
            .from_(vote)\
            .select(select_content)\
            .where(vote.vote_id == vote_id))