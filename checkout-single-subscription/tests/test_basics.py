import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):  # Flask WebDev, 2nd Edition, p. 118
    def setUp(self):
        """1. The setUp() method creates an app configured
        for testing, and activates the application context.
        2. Creates a new database for the test by
        calling db.create_all() method"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """1. The tearDown() method removes the
        application & database context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """Ensures that the app is configured correctly for testing."""
        self.assertTrue(current_app.config['TESTING'])