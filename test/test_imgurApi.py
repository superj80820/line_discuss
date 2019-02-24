import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from setting import *
from model.imgurApi import imgurApi
import unittest
import time

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.imgurApiModel = imgurApi(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN)

    def test_upload(self):
        print(self._testMethodName)
        print(self.imgurApiModel.upload("../res/test.jpg"))

if __name__ == '__main__':
    unittest.main()