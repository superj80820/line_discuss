import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.computerIO import computerIO
import unittest

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.computerIOModel = computerIO()

    def test_click(self):
        print(self._testMethodName)
        print(self.computerIOModel.screenshop())

if __name__ == '__main__':
    unittest.main()
