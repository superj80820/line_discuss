import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.processImage import processImage
from model.discussFigure import discussFigure
from model.computerIO import computerIO
import threading
from socketIO_client import SocketIO, LoggingNamespace
import random
import time
import keyboard

class websocketClient(object):
    def __init__(self, room_id=None, url="localhost", port=5000):
        self.socketIO = SocketIO(url, port, LoggingNamespace)
        self.computerIOModel = computerIO()
        self.processImageModel = processImage()
        self.room_id = room_id or self.getRandId()
        self.vote_id = None
        self.thread_running = True
        self.rollCallTriggerAndRes = False
        self.voteStopTriggerAndRes = False
        self.discussImageTriggerAndRes = False
        print("websocketClient is running url: %s, port: %s, room_id: %s" %(url, port, room_id))

    def emit(self, on_content, value=None):
        self.socketIO.emit(on_content, value)

    def getRoomId(self):
        return self.room_id
    
    def getRandId(self):
        return ''.join(["%s" % random.randint(0, 9) for num in range(6)])

    def createVote(self):
        self.vote_id = self.getRandId()

    def getVoteId(self):
        return self.vote_id

    def thread(self):
        def screenshop_requests(*args):
            print(args)
            image_content = self.processImageModel.PILimageToBase64(
                self.computerIOModel.screenshop()
            )
            self.socketIO.emit('screenshop_revice', {
                "image": image_content, "user_id": args[0]["user_id"]
            })
        def rollCall_response(*args):
            print(args)
            self.rollCallTriggerAndRes = args
        def vote_response(*args):
            print(args)
            self.voteStopTriggerAndRes = args
        def discussImage_response(*args):
            print(args)
            self.discussImageTriggerAndRes = args

        while self.thread_running:
            self.socketIO.on('screenshop_requests', screenshop_requests)
            self.socketIO.on('rollCall_response', rollCall_response)
            self.socketIO.on('vote_response', vote_response)
            self.socketIO.on('discussImage_response', discussImage_response)
            self.socketIO.wait(seconds=3)
        return

    def threadStop(self):
        self.thread_running = False
    
    def waitRollCallTrigger(self):
        while self.rollCallTriggerAndRes == False:
            time.sleep(1)
        ret = self.rollCallTriggerAndRes
        self.rollCallTriggerAndRes = False
        return ret

    def waitVoteStopTrigger(self):
        while self.voteStopTriggerAndRes == False:
            time.sleep(1)
        ret = self.voteStopTriggerAndRes
        self.voteStopTriggerAndRes = False
        return ret

    def waitDiscussImageTrigger(self):
        while self.discussImageTriggerAndRes == False:
            time.sleep(1)
        ret = self.discussImageTriggerAndRes
        self.discussImageTriggerAndRes = False
        return ret

    def send2Audience(self, room_id):
        image_content = self.processImageModel.PILimageToBase64(
            self.computerIOModel.screenshop()
        )
        self.socketIO.emit('send2Audience', {"image": image_content, "room_id": room_id})

    def rollCall(self):
        self.emit("rollCall", {"room_id": self.getRoomId()})

    def voteStar(self):
        self.emit("vote", {"action": "start", "room_id": self.getRoomId(), "vote_id": self.getVoteId()})

    def voteStop(self):
        self.emit("vote", {"action": "stop", "room_id": self.getRoomId(), "vote_id": self.getVoteId()})

    def discussImage(self):
        self.emit("discussImage", {"room_id": self.getRoomId()})