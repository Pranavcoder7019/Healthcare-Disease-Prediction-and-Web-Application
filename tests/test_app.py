import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_predict_invalid_method(self):
        result = self.app.get('/predict')
        self.assertEqual(result.status_code, 405)

if __name__ == '__main__':
    unittest.main()
