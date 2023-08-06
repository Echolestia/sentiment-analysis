import random
import string

import unittest
import json
import string
import random
from app import app


# List of seed words to help generate sentences
SEED_WORDS = ["happy", "sad", "angry", "joyful",
              "disappointed", "excited", "terrible", "great"]


def generate_random_sentence():
    length = random.randint(1, 50)  # Length of the sentence
    # Generate the sentence
    sentence = ' '.join(random.choices(SEED_WORDS, k=length))

    # Randomly capitalize words
    sentence = ' '.join(word.upper() if random.random() <
                        0.2 else word for word in sentence.split())

    # Randomly add punctuation
    # Space is more likely than other punctuation
    punctuation = string.punctuation + ' '*10
    sentence = ''.join(c + random.choice(punctuation)
                       if random.random() < 0.1 else c for c in sentence)

    return sentence


class FuzzTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_fuzzing(self):
        for _ in range(100):  # Number of fuzzing attempts
            length = random.randint(0, 1000)  # Length of the random string
            # Generate a random string
            fuzz = generate_random_sentence()

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
