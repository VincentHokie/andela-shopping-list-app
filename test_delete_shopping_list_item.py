__author__ = 'MacUser'

from flask import session, url_for
from app import app
import unittest
from datetime import datetime


class DeleteShoppingListItemTests(unittest.TestCase):

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

    def test_delete_shopping_list_item_functionality(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                username="vince",
                password="123"), follow_redirects=True)

            rv3 = client.post('/create/shopping-list/item', data=dict(
                name="Babythings", shopping_list=1), follow_redirects=True)

            lists = session["shopping-list-items"]
            gotten_object = None
            for key in lists:
                gotten_object = lists[key]
                break

            rv4 = client.post('/delete/shopping-list-item', data=dict(
                id=gotten_object["id"]), follow_redirects=True)

            self.assertEqual(
                rv.status_code, 200,
                "The sign up page was not loaded as expected")
            self.assertEqual(
                rv2.status_code, 200,
                "The login page was not loaded as expected")
            self.assertEqual(
                rv3.status_code, 200,
                "The create shopping list page was not loaded as expected")
            self.assertNotIn(gotten_object["id"], session["shopping-list-items"],
                "The shopping list item has not been deleted as expected")

    def test_delete_shopping_list_as_guest_functionality(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                username="vince",
                password="123"), follow_redirects=True)

            rv3 = client.post('/create/shopping-list/item', data=dict(
                name="Babythings", shopping_list=1), follow_redirects=True)

            rv4 = client.get('/logout')

            lists = session["shopping-list-items"]
            gotten_object = None
            for key in lists:
                gotten_object = lists[key]
                break

            rv5 = client.post('/delete/shopping-list-item', data=dict(
                id=gotten_object["id"]), follow_redirects=True)

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
                    rv4.status_code, 302,
                    "The logout page was not loaded as expected")
            self.assertIn(gotten_object["id"], session["shopping-list-items"],
                "The shopping list item has been deleted by a guest user")

    def test_delete_shopping_list_id_required(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                username="vince",
                password="123"), follow_redirects=True)

            rv3 = client.post('/create/shopping-list/item', data=dict(
                name="Babythings", shopping_list=1), follow_redirects=True)

            rv4 = client.get('/logout')

            lists = session["shopping-list-items"]
            gotten_object = None
            for key in lists:
                gotten_object = lists[key]
                break

            rv5 = client.post('/delete/shopping-list-item', follow_redirects=True)

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
                    rv4.status_code, 302,
                    "The logout page was not loaded as expected")
            self.assertIn(gotten_object["id"], session["shopping-list-items"],
                "The shopping list item has been deleted without its id")