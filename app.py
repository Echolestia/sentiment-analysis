from flask import Flask, request, jsonify
from joblib import load
import spacy

app = Flask(__name__)

# load the model from the file
regressor = load('regressor_model_continuous.joblib')
vectorizer = load('vectorizer_continuous.joblib')

nlp = spacy.load('en_core_web_sm')


def preprocess_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])


@app.route('/predict', methods=['POST'])
def predict():
    # Receive the data from client
    data = request.get_json(force=True)

        # Handle empty input data
    if not data:
        return jsonify([])


    # Preprocess the incoming data
    preprocessed_samples = [preprocess_text(sentence) for sentence in data]

    # Vectorize sentences using the loaded vectorizer
    sample_vectors = vectorizer.transform(preprocessed_samples)

    # Predict sentiment using the loaded SVM classifier
    predicted_values = regressor.predict(sample_vectors)

    # Clip output value between 0 and 1
    predicted_values = [max(min(value, 1), 0) for value in predicted_values]

    # Return results in a response object
    return jsonify(predicted_values)


# if __name__ == '__main__':
#     app.run(port=5000, debug=False)
