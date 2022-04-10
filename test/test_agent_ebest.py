import unittest
from ..agent import ebest
import inspect
import time


class TestEBest(unittest.TestCase):
    def setUp(self):
        self.ebest = ebest("DEMO")
        self.ebest.login()

    def tearDown(self):
        self.ebest.logout()

if __name__ == '__main__':
    test = TestEBest()
    test.setUp()
    test.tearDown()

