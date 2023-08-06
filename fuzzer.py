import unittest
import json
import string
import random
from app import app


class FuzzTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_fuzzing(self):
        for _ in range(100):  # Number of fuzzing attempts
            length = random.randint(0, 1000)  # Length of the random string
            # Generate a random string
            fuzz = ''.join(random.choices(string.printable, k=length))

            print(f'Fuzzing with input:\n{fuzz}\n')  # Print the input

            # Send the fuzz as input to your API endpoint
            response = self.client.post('/predict',
                                        data=json.dumps([fuzz]),
                                        content_type='application/json')

            # Print the response
            print(
                f'Response:\nStatus code: {response.status_code}\nData: {response.data}\n')

            # Check that the server doesn't return a 5xx error (internal server error)
            self.assertNotIn(response.status_code, range(500, 600))


if __name__ == '__main__':
    unittest.main()
