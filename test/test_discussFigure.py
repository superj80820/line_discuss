import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.discussFigure import discussFigure
import unittest

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.discussFigureModel = discussFigure()

    def test_vote(self):
        print(self._testMethodName)
        vote_item1 = {"name": "Yes", "value": 3}
        vote_item2 = {"name": "No~", "value": 4}
        self.discussFigureModel.vote(vote_item1, vote_item2)

    def test_rollCall(self):
        print(self._testMethodName)
        present = {"name": "present", "value": 4}
        absent = {"name": "absent", "value": 8}
        late = {"name": "late", "value": 2}
        excused = {"name": "excused", "value": 10}
        self.discussFigureModel.rollCall(present, absent, late, excused)

    def test_discussImage(self):
        print(self._testMethodName)
        image_path = "../res/perspective.jpg"
        self.discussFigureModel.discussImage(image_path, "請問你這裡的理論是甚麼?")

if __name__ == '__main__':
    unittest.main()
