__author__ = 'MacUser'

from flask import session
from app import app
import unittest


class LoginTests(unittest.TestCase):

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

    def test_sign_up_functionality(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            exists = False
            users = session["users"]

            for key in users:
                user = users[key]
                print(user["email"])
                if user["username"] == "vince" and \
                        user["email"] == "vincenthokie@gmail.com" and \
                        user["password"] == "123":
                    exists = True
                    break

            self.assertEqual(
                rv.status_code, 200, "The page was not correctly loaded")
            self.assertEqual(exists, True, "The user was not created")

    def test_sign_up_username_required(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                email="vincenthokie@gmail.com",
                password="123",
                password2="123"), follow_redirects=True)

            exists = False
            users = session["users"]

            for key in users:
                user = users[key]
                if user["username"] == "vince" and \
                        user["email"] == "vincenthokie@gmail.com" and \
                        user["password"] == "123":
                    exists = True
                    break

            self.assertEqual(rv.status_code, 200,
                             "The page was not correctly loaded")
            self.assertEqual(
                exists, False,
                "The user was created desipite not having a username")

    def test_sign_up_email_required(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                password="123",
                password2="123"), follow_redirects=True)

            exists = False
            users = session["users"]

            for key in users:
                user = users[key]
                if user["username"] == "vince" and \
                        user["email"] == "vincenthokie@gmail.com" and \
                        user["password"] == "123":
                    exists = True
                    break

            self.assertEqual(
                rv.status_code, 200, "The page was not correctly loaded")
            self.assertEqual(
                exists, False,
                "The user was created desipite not having a username")

    def test_sign_up_password_required(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password2="123"), follow_redirects=True)

            exists = False
            users = session["users"]

            for key in users:
                user = users[key]
                if user["username"] == "vince" and \
                        user["email"] == "vincenthokie@gmail.com" and \
                        user["password"] == "123":
                    exists = True
                    break

            self.assertEqual(
                rv.status_code, 200, "The page was not correctly loaded")
            self.assertEqual(
                exists, False,
                "The user was created desipite not having a username")

    def test_sign_up_password_conf_required(self):

        with app.test_client() as client:
            rv = client.post('/sign-up', data=dict(
                username="vince",
                email="vincenthokie@gmail.com",
                password2="123"), follow_redirects=True)

            exists = False
            users = session["users"]

            for key in users:
                user = users[key]
                if user["username"] == "vince" and \
                        user["email"] == "vincenthokie@gmail.com" and \
                        user["password"] == "123":
                    exists = True
                    break

            self.assertEqual(
                rv.status_code, 200, "The page was not correctly loaded")
            self.assertEqual(
                exists, False,
                "The user was created desipite not having a username")
