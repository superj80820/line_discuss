import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.processImage import processImage
from model.computerIO import computerIO
import unittest

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.computerIOModel = computerIO()
        self.processImageModel = processImage()

    def test_detection(self):
        print(self._testMethodName)
        print(self.processImageModel.PILimageToBase64(
            self.computerIOModel.screenshop())
        )

if __name__ == '__main__':
    unittest.main()
