import os 
import pandas as pd 
import numpy as np
from src.logger import logging 
import nltk 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.preprocessing import LabelEncoder 
import re


def transformation(content):
    try:
        stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
        stemmed_content = stemmed_content.lower()
        stemmed_content = stemmed_content.split()
        port_stem = PorterStemmer()
        stop_words = set(stopwords.words('english'))  # Avoid loading inside list comprehension
        stemmed_content = [port_stem.stem(word) for word in stemmed_content if word not in stop_words]
        return ' '.join(stemmed_content)
    except Exception as e:
        logging.error("Some error occurred: %s", str(e))
        return ""  # Return empty string on error to avoid None


def preprocess(df):
    try:
        df = df.copy()
        df.rename(columns={'Category': 'target', 'Message': 'text'}, inplace=True)

        if 'target' in df.columns:
            encoder = LabelEncoder()
            df['target'] = encoder.fit_transform(df['target'])
            logging.debug('Target column encoded successfully')
        else:
            raise KeyError("Column 'Category' not found in dataframe")

        df['text'] = df['text'].apply(transformation)

        # Convert invalid or blank strings to np.nan
        df['text'] = df['text'].apply(lambda x: np.nan if str(x).strip().lower() in ['nan', 'null', ''] else x)

        logging.debug('Handling missing values')
        df.dropna(inplace=True)

        logging.debug('Text column transformed successfully')

        return df
    except Exception as e:
        logging.error('Error in preprocessing: %s', str(e))
        return df


def save_data(train_data, test_data, data_path):
    try:
        logging.debug(f"Saving data to {data_path}")
        data_path = os.path.join(data_path, 'interim')
        os.makedirs(data_path, exist_ok=True)

        train_data.to_csv(os.path.join(data_path, 'preprocessed_train_data.csv'), index=False)
        test_data.to_csv(os.path.join(data_path, 'preprocessed_test_data.csv'), index=False)

        logging.debug("Data saved successfully.")
    except Exception as e:
        logging.error("Error saving data: %s", str(e))


def main():
    try:
        nltk.download('stopwords')
        logging.debug('Stopwords downloaded')
    except Exception as e:
        logging.error('Unable to download stopwords: %s', str(e))

    try:
        train_df = pd.read_csv('./data/raw/train_data.csv')
        test_df = pd.read_csv('./data/raw/test_data.csv')  # Changed from train_data.csv to test_data.csv
        logging.debug('Data loaded successfully')

        train_df_preprocessed = preprocess(train_df)
        test_df_preprocessed = preprocess(test_df)

        logging.debug('Data processed successfully')

        path = './data'
        save_data(train_df_preprocessed, test_df_preprocessed, path)

    except Exception as e:
        logging.error('Main execution failed: %s', str(e))


if __name__ == "__main__":
    main()
