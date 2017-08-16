__author__ = 'MacUser'

from flask import session, url_for
from app import app
import unittest
from datetime import datetime


class URLAccessTests(unittest.TestCase):

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

    def test_login_page_access(self):

        with app.test_client() as client:
            rv = client.get('/login')

            self.assertEqual(
                rv.status_code, 200,
                "The login page was not loaded as expected")

    def test_sign_up_page_access(self):

        with app.test_client() as client:
            rv = client.get('/sign-up')

            self.assertEqual(
                rv.status_code, 200,
                "The sign up page was not loaded as expected")

    def test_create_shopping_list_page_access(self):

        with app.test_client() as client:
            rv = client.get('/create/shopping-list')

            self.assertEqual(
                rv.status_code, 302,
                "The create shopping list page loaded as guest user")

    def test_view_shopping_list_page_access(self):

        with app.test_client() as client:
            rv = client.get('/view/shopping-lists')

            self.assertEqual(
                rv.status_code, 302,
                "The view shopping lists page loaded as guest user")

    def test_create_shopping_list_page_access(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                username="vince",
                password="123"), follow_redirects=True)

            rv3 = client.get('/create/shopping-list')

            self.assertEqual(
                rv3.status_code, 200,
                "The create shopping list page was not loaded as expected")

    def test_view_shopping_list_page_access(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                username="vince",
                password="123"), follow_redirects=True)

            rv3 = client.get('/view/shopping-lists')

            self.assertEqual(
                rv3.status_code, 200,
                "The view shopping lists page was not loaded as expected")

    def test_home_page_access(self):

        with app.test_client() as client:
            rv = client.get('/')

            self.assertEqual(
                rv.status_code, 200,
                "The home page was not loaded as expected")