from flask_testing import TestCase
from main import app
from flask import current_app
from flask import url_for

class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] =True
        app.config['WTF_CSRF_ENABLED'] =False
        return app

    def test_app_exists(self):
        # Da ok
        self.assertIsNotNone(current_app) 

        # Da Failure
        #self.assertIsNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    # Probar si Index redirige a hello
    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('hello'))

    # Probar si hello regresa un 200
    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        self.assert200(response)

    # Probar un post
    def test_hello_post(self):
        fake_form = {
                'username': 'fake',
                'password': 'fake-password'
                }
        response = self.client.post(url_for('hello'),data=fake_form)
        self.assertRedirects(response, url_for('index'))

    # Probar Blueprints
    def test_auth_blueprint_exits(self):
        self.assertIn('auth', self.app.blueprints)
