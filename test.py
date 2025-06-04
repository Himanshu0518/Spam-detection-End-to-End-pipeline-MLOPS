import joblib
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('stopwords')

def transformation(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower().split()
    port_stem = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    transformed = [port_stem.stem(word) for word in text if word not in stop_words]
    return ' '.join(transformed)

def predict_single(text, vectorizer, model):
    transformed = transformation(text)
    vector = vectorizer.transform([transformed])
    feature_names = vectorizer.get_feature_names_out()
    vector_df = pd.DataFrame(vector.toarray(), columns=feature_names)
    prediction = model.predict(vector_df)
    return prediction[0]

if __name__ == "__main__":
    # Load model and vectorizer
    vectorizer = joblib.load('./models/vectorizer.joblib')
    model = joblib.load('./models/RandomForest.joblib')

    test_samples = {
        "spam": [
            "Congratulations, you have won a free lottery! Click here to claim your prize",
            "You have been selected for a cash reward. Call now!",
        ],
        "ham": [
            "Hey, are we still meeting for dinner tomorrow?",
            "Please find the attached report from last week’s meeting.",
            "Can you send me the files by today?",
        ]
    }

    print("Testing spam examples:")
    for text in test_samples["spam"]:
        pred = predict_single(text, vectorizer, model)
        label = "spam" if pred == 1 else "ham"
        print(f"Text: {text}\nPrediction: {label}\n")

    print("Testing ham examples:")
    for text in test_samples["ham"]:
        pred = predict_single(text, vectorizer, model)
        label = "spam" if pred == 1 else "ham"
        print(f"Text: {text}\nPrediction: {label}\n")
