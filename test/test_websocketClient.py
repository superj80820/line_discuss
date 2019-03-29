import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.websocketClient import websocketClient
import time
import threading
import unittest


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.websocketClientModel = websocketClient("123456")

    # def test_emit_create_room(self):
    #     print(self._testMethodName)
    #     self.websocketClientModel.emit("create_room", self.websocketClientModel.getRoomId())

    # def test_emit_vote(self):
    #     print(self._testMethodName)
    #     print(self.websocketClientModel.getRoomId())
    #     # self.websocketClientModel.createVote()
    #     self.websocketClientModel.emit("create_room", self.websocketClientModel.getRoomId())
    #     # self.websocketClientModel.emit("vote", {"action": "start", "room_id": self.websocketClientModel.getRoomId(), "vote_id": self.websocketClientModel.getVoteId()})
    #     self.websocketClientModel.thread()
    #     time.sleep(10)
    #     self.websocketClientModel.emit("vote", {"action": "stop", "room_id": self.websocketClientModel.getRoomId(), "vote_id": self.websocketClientModel.getVoteId()})

    # def test_thread(self):
    #     self.websocketClientModel.emit("create_room", self.websocketClientModel.getRoomId())
    #     self.websocketClientModel.thread()

    # def test_send2Audience(self):
    #     self.websocketClientModel.send2Audience(self.websocketClientModel.getRoomId())

    def test_rollCall(self):
        self.websocketClientModel.emit("create_room", self.websocketClientModel.getRoomId())
        self.websocketClientModel.rollCall()
        self.websocketClientModel.thread()

if __name__ == '__main__':
    unittest.main()
