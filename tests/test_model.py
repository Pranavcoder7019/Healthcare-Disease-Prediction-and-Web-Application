import unittest
import os
import joblib

class ModelTestCase(unittest.TestCase):
    def test_model_files_exist(self):
        self.assertTrue(os.path.exists('healthcare_model.pkl'))
        self.assertTrue(os.path.exists('scaler.pkl'))
        self.assertTrue(os.path.exists('encoder.pkl'))

    def test_model_loading(self):
        model = joblib.load('healthcare_model.pkl')
        self.assertIsNotNone(model)

if __name__ == '__main__':
    unittest.main()
