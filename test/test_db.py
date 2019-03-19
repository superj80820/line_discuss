import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.db import db
import unittest
import time

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.dbModel = db()

    # def test_insertDiscussQuery(self):
    #     print(self._testMethodName)
    #     timestamp = time.time()
    #     print(self.dbModel.insertDiscussQuery("base64asdfasfd", "這個問題請問是?", timestamp))

    # def test_insertStatusQuery(self):
    #     print(self._testMethodName)
    #     print(self.dbModel.insertStatusQuery("5678asdf678d", "discuss"))

    # def test_updateStatusQuery(self):
    #     print(self._testMethodName)
    #     print(self.dbModel.updateStatusQuery("action", "no discuss", "where", "whdereasdf"))

    # def test_selectStatusQuery(self):
    #     print(self._testMethodName)
    #     print(self.dbModel.selectStatusQuery("5678asdf678d", "action"))
    #     print(self.dbModel.selectStatusQuery("5678asdf678d", "user_id"))

    # def test_updateLastDiscussQuery(self):
    #     print(self._testMethodName)
    #     print(self.dbModel.updateLastDiscussQuery("5678asdf678d", "image", "base64asfdsdf"))

    # def test_selectVote(self):
    #     print(self._testMethodName)
    #     print(self.dbModel.selectVote("551950", "vote_data"))

    # def test_selectRoom(self):
    #     print(self._testMethodName)
    #     print(self.dbModel.selectRoom("123456", "members"))

    def test_selectStatusRoomIdMembers(self):
        print(self._testMethodName)
        print(self.dbModel.selectStatusRoomIdMembers("123456"))

if __name__ == '__main__':
    unittest.main()