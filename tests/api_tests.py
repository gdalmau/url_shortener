import unittest

from url_shortener.utils import validate_shortcode, generate_shortcode


class UtilsTest(unittest.TestCase):
    def test_validate_shortcodes(self):
        self.assertEqual(validate_shortcode('asdfgh'), True)
        self.assertEqual(validate_shortcode('123456'), True)
        self.assertEqual(validate_shortcode('______'), True)
        self.assertEqual(validate_shortcode('test1_'), True)

        self.assertEqual(validate_shortcode('12345-'), False)
        self.assertEqual(validate_shortcode('12345'), False)
        self.assertEqual(validate_shortcode('123456'), True)
        self.assertEqual(validate_shortcode('1234567'), False)

    def test_generate_shortcode(self):
        for len in range(1, 10):
            shortcode = generate_shortcode(length=len)
            self.assertEqual(validate_shortcode(shortcode, length=len), True)


class ApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'TESTING': True,
        }
        from url_shortener.config import app, db, configure_db, configure_api
        app.config.update(config)
        cls.app = app
        cls.test_app = app.test_client()
        with app.app_context():
            configure_api(app)
            configure_db(db)

    def test_get_unexisting_url(self):
        with self.app.app_context():
            resp = self.test_app.get('/test12')
            self.assertEqual(resp.status_code, 404)

    def test_get_stats_unexisting_url(self):
        with self.app.app_context():
            resp = self.test_app.get('/test12/stats')
            self.assertEqual(resp.status_code, 404)

    def create_url(self, url, shortcode):
        from url_shortener.api import create_shortened_url
        # self.test_app.post('/shorten', data=dict(url=url, shortcode=shortcode))
        return create_shortened_url(url, shortcode)

    @unittest.skip
    def test_shorten_without_url(self):
        with self.app.app_context():
            resp = self.create_url(None, '123456')
            self.assertEqual(resp.status_code, 409)

    @unittest.skip
    def test_shorten_invalid_shortcode(self):
        with self.app.app_context():
            resp = self.create_url('http://www.google.com', '1234567')
            self.assertEqual(resp.status_code, 412)

    def test_shorten_url(self):
        with self.app.app_context():
            url, shortcode = 'http://www.google.com', 'google'
            resp = self.create_url(url, shortcode)
            self.assertEqual(resp.json['shortcode'], shortcode)

            resp = self.test_app.get('/google/stats')
            json_data = resp.json
            self.assertIn('created', json_data)
            self.assertIn('lastRedirect', json_data)
            self.assertEqual(json_data.get('lastRedirect', True), None)
            self.assertIn('redirectCount', json_data)
            self.assertEqual(json_data['redirectCount'], 0)

    def test_redirect_count_increase(self):
        with self.app.app_context():
            url, shortcode = 'http://www.example.com', 'examp1'
            resp = self.create_url(url, shortcode)
            self.assertEqual(resp.json['shortcode'], shortcode)

            resp = self.test_app.get('/examp1/stats')
            json_data = resp.json
            self.assertIn('created', json_data)
            self.assertIn('lastRedirect', json_data)
            self.assertEqual(json_data.get('lastRedirect', True), None)
            self.assertIn('redirectCount', json_data)
            self.assertEqual(json_data['redirectCount'], 0)

            resp = self.test_app.get('/examp1')
            resp = self.test_app.get('/examp1/stats')
            json_data = resp.json
            self.assertIn('created', json_data)
            self.assertIn('lastRedirect', json_data)
            self.assertNotEqual(json_data.get('lastRedirect', True), None)
            self.assertIn('redirectCount', json_data)
            self.assertEqual(json_data['redirectCount'], 1)
