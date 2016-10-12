import unittest
import webtest
import os
from server import app

class BaseWebTest(unittest.TestCase):
    """Base Web Test to test openprocurement.relocation.api.
    It setups the database before each test and delete it after.
    """
    initial_auth = ('Basic', ('broker', ''))
    relative_to = os.path.dirname(__file__)

    @classmethod
    def setUpClass(cls):
        while True:
            try:
                cls.app = webtest.TestApp(app)
            except:
                pass
            else:
                break

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_test1(self):
        response = self.app.get('/test1', {})
        self.assertEqual(response.status, "200 OK")

    def test_test2(self):
        response = self.app.get('/test2', {})
        self.assertEqual(response.status, "200 OK")

    def test_test3(self):
        response = self.app.get('/test3', {}, status = "409 Conflict")
        self.assertEqual(response.status, "409 Conflict")
