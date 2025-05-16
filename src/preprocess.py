import os 
import pandas as pd 
import numpy as np
import logging 
import nltk 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.preprocessing import LabelEncoder 
import re
import yaml 

# Setup logger
logger = logging.getLogger('preprocess')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('./logs/data_preprocessing.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


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
        logger.error("Some error occurred: %s", str(e))
        return ""  # Return empty string on error to avoid None


def preprocess(df):
    try:
        df = df.copy()
        df.rename(columns={'Category': 'target', 'Message': 'text'}, inplace=True)

        if 'target' in df.columns:
            encoder = LabelEncoder()
            df['target'] = encoder.fit_transform(df['target'])
            logger.debug('Target column encoded successfully')
        else:
            raise KeyError("Column 'Category' not found in dataframe")

        df['text'] = df['text'].apply(transformation)

        # Convert invalid or blank strings to np.nan
        df['text'] = df['text'].apply(lambda x: np.nan if str(x).strip().lower() in ['nan', 'null', ''] else x)

        logger.debug('Handling missing values')
        df.dropna(inplace=True)

        logger.debug('Text column transformed successfully')

        return df
    except Exception as e:
        logger.error('Error in preprocessing: %s', str(e))
        return df


def save_data(train_data, test_data, data_path):
    try:
        logger.debug(f"Saving data to {data_path}")
        data_path = os.path.join(data_path, 'interim')
        os.makedirs(data_path, exist_ok=True)

        train_data.to_csv(os.path.join(data_path, 'preprocessed_train_data.csv'), index=False)
        test_data.to_csv(os.path.join(data_path, 'preprocessed_test_data.csv'), index=False)

        logger.debug("Data saved successfully.")
    except Exception as e:
        logger.error("Error saving data: %s", str(e))


def main():
    try:
        nltk.download('stopwords')
        logger.debug('Stopwords downloaded')
    except Exception as e:
        logger.error('Unable to download stopwords: %s', str(e))

    try:
        train_df = pd.read_csv('./data/raw/train_data.csv')
        test_df = pd.read_csv('./data/raw/test_data.csv')  # Changed from train_data.csv to test_data.csv
        logger.debug('Data loaded successfully')

        train_df_preprocessed = preprocess(train_df)
        test_df_preprocessed = preprocess(test_df)

        logger.debug('Data processed successfully')

        path = './data'
        save_data(train_df_preprocessed, test_df_preprocessed, path)

    except Exception as e:
        logger.error('Main execution failed: %s', str(e))


if __name__ == "__main__":
    main()
