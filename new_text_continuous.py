from joblib import load
import spacy

# load the model from the file
regressor = load('regressor_model_continuous.joblib')
vectorizer = load('vectorizer_continuous.joblib')

nlp = spacy.load('en_core_web_sm')


def preprocess_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])


# test sentences
sample_sentences = ["Wow you look amazing", "Great work man!!",
                    "I hate my life",
                    "okay can",
                    "I like to die",
                    "I love to hurt myself",
                    "hi, my name is john"]

# Preprocess sample sentences
preprocessed_samples = [preprocess_text(
    sentence) for sentence in sample_sentences]

# Vectorize sentences using the same loaded vectorizer
sample_vectors = vectorizer.transform(preprocessed_samples)

# Predict sentiment using the loaded SVM classifier
predicted_values = regressor.predict(sample_vectors)

for sentence, value in zip(sample_sentences, predicted_values):
    if value > 1:
        value = 1
    if value < 0:
        value = 0
    print(f"Sentence: {sentence}")
    print(f"Predicted value: {value}")
