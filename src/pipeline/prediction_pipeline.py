import pandas as pd
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from src.logger import logging
import os

nltk.download('stopwords', quiet=True)

class SpamClassifier:
    def __init__(self):
        self.vectorizer_path = os.path.join("models", "vectorizer.joblib")
        self.model_path = os.path.join("models", "RandomForest.joblib")
        self.vectorizer = joblib.load(self.vectorizer_path)
        self.model = joblib.load(self.model_path)
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()

    def transformation(self,text):
        text = re.sub('[^a-zA-Z]', ' ', text)
        text = text.lower().split()
        port_stem = PorterStemmer()
        transformed = [port_stem.stem(word) for word in text if word not in self.stop_words]
        return ' '.join(transformed)

    def predict_single(self , text ):
        transformed = self.transformation(text)
        vector = self.vectorizer.transform([transformed])
        feature_names = self.vectorizer.get_feature_names_out()
        vector_df = pd.DataFrame(vector.toarray(), columns=feature_names)
        prediction = self.model.predict(vector_df)
        return prediction[0]


# # For standalone testing
# if __name__ == "__main__":
#     classifier = SpamClassifier()
#     sample = "Congratulations! You've won a prize."
#     result = classifier.predict(sample)
#     print("Spam" if result == 0 else "Ham")
