import unittest
import json
from app import app
from app import preprocess_text


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_predict_positive_statements(self):
        response = self.client.post('/predict',
                                    data=json.dumps(
                                        ["Good job", "I am happy"]),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertTrue(all(0.5 < d <= 1 for d in data))

    def test_predict_negative_statements(self):
        response = self.client.post('/predict',
                                    data=json.dumps(
                                        ["I am feeling down", "I hate this"]),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertTrue(all(0 <= d < 0.5 for d in data))

    def test_predict_mixed_statements(self):
        response = self.client.post('/predict',
                                    data=json.dumps(
                                        ["I am feeling down", "Good job"]),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertTrue(0 <= data[0] < 0.5 and 0.5 < data[1] <= 1)

    def test_predict_empty_list(self):
        response = self.client.post('/predict',
                                    data=json.dumps([]),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

    def test_predict_no_data(self):
        response = self.client.post('/predict',
                                    data=None,
                                    content_type='application/json')
        # 400 Bad Request
        self.assertEqual(response.status_code, 400)

    def test_predict_non_json(self):
        response = self.client.post('/predict',
                                    data='This is not json',
                                    content_type='application/json')
        # 400 Bad Request
        self.assertEqual(response.status_code, 400)

    def test_preprocess_text(self):
        result = preprocess_text("I am not a happy person")
        self.assertEqual(result, "happy person")

    def test_normal_text(self):
        self.assertEqual(preprocess_text(
            "I am a happy person."), "happy person")

    def test_text_with_punctuation(self):
        self.assertEqual(preprocess_text(
            "I am a happy person!"), "happy person")

    def test_text_with_numbers(self):
        self.assertEqual(preprocess_text(
            "I am the 1st happy person."), "happy person")

    def test_empty_text(self):
        self.assertEqual(preprocess_text(""), "")

    def test_text_with_stop_words_only(self):
        self.assertEqual(preprocess_text("a is the of and"), "")

    def test_text_with_non_alphabetic_characters(self):
        self.assertEqual(preprocess_text(
            "I am @happy #person."), "person")


if __name__ == '__main__':
    unittest.main()
