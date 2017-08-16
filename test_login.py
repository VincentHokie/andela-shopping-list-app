__author__ = 'MacUser'

from flask import session, url_for
from app import app
import unittest


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

    def test_login_functionality(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                username="vince",
                password="123"), follow_redirects=True)

            logged_in = session["logged_in"]

            self.assertEqual(
                rv.status_code, 200,
                "The sign up page was not loaded as expected")
            self.assertEqual(
                rv2.status_code, 200,
                "The login page was not loaded as expected")
            self.assertNotEqual(None, logged_in,
                                "The user was not logged in")
            self.assertNotEqual(None, logged_in["id"],
                                "The user was not logged in")
            self.assertNotEqual(None, logged_in["username"],
                                "The user was not logged in")

    def test_wrong_details_login_functionality(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                username="vincee",
                password="123"), follow_redirects=True)

            logged_in = session["logged_in"]

            self.assertEqual(
                rv.status_code, 200,
                "The sign up page was not loaded as expected")
            self.assertEqual(
                rv2.status_code, 200,
                "The login page was not loaded as expected")
            self.assertEqual(None, logged_in, "The user was not logged in")

    def test_wrong_details_login_functionality2(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                username="vince",
                password="1233"), follow_redirects=True)

            logged_in = session["logged_in"]

            self.assertEqual(
                rv.status_code, 200,
                "The sign up page was not loaded as expected")
            self.assertEqual(
                rv2.status_code, 200,
                "The login page was not loaded as expected")
            self.assertEqual(None, logged_in, "The user was not logged in")

    def test_login_username_required(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                password="123"), follow_redirects=True)

            logged_in = session["logged_in"]

            self.assertEqual(
                rv.status_code, 200,
                "The sign up page was not loaded as expected")
            self.assertEqual(
                rv2.status_code, 200,
                "The login page was not loaded as expected")
            self.assertEqual(
                None, logged_in,
                "The user was not logged in without a username")

    def test_login_email_required(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            rv2 = client.post('/login', data=dict(
                username="vince"), follow_redirects=True)

            logged_in = session["logged_in"]

            self.assertEqual(
                rv.status_code, 200,
                "The sign up page was not loaded as expected")
            self.assertEqual(
                rv2.status_code, 200,
                "The login page was not loaded as expected")
            self.assertEqual(
                None, logged_in,
                "The user was not logged in without a password")