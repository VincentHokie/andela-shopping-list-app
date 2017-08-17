__author__ = 'MacUser'

from flask import session, url_for
from app import app
import unittest
from datetime import datetime


class SignUpTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False

        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_update_shopping_list_functionality(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                username="vince",
                password="123"), follow_redirects=True)

            rv3 = client.post('/create/shopping-list', data=dict(
                name="Babythings"), follow_redirects=True)

            lists = session["shopping-lists"]

            shopping_list = False
            for key in lists:
                shopping_list = lists[key]
                break

            rv4 = client.post('/update/shopping-list/'+shopping_list["id"], data=dict(
                name="Babythings1"), follow_redirects=True)

            lists = session["shopping-lists"]
            exists = False

            for key in lists:
                shopping_list = lists[key]
                if shopping_list["name"] == "Babythings1" and\
                    datetime.now() > datetime.strptime(shopping_list["time"],
                   "%Y-%b-%d %H:%M"):
                    exists = True
                    break

            self.assertEqual(
                rv.status_code, 200, 
                "The sign up page was not loaded as expected")
            self.assertEqual(
                rv2.status_code, 200, 
                "The login page was not loaded as expected")
            self.assertEqual(
                rv3.status_code, 200, 
                "The create shopping list page was not loaded as expected")
            self.assertEqual(
                True, exists, 
                "The shopping list has not been created as expected")