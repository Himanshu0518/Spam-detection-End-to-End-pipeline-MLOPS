import os 
import pandas as pd 
import logging 
from sklearn.feature_extraction.text import TfidfVectorizer
import yaml

# Setup logging
os.makedirs('./logs', exist_ok=True)

logger = logging.getLogger('feature_engineering')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('./logs/feature_engineering.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def load_params(file_path='params.yaml'):
    try:
        with open(file_path, 'r') as f:
            params = yaml.safe_load(f)
        return params
    except Exception as e:
        print(f"Error loading parameters from {file_path}: {e}")
        return None

# Load preprocessed data
def load_data(file_path):
    try:
        logger.debug(f"Loading data from {file_path}")
        data = pd.read_csv(file_path)
        logger.debug(f"Data loaded successfully. Shape: {data.shape}")
        return data
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return None

# Extract TF-IDF features
def feature_extraction(train_df, test_df,max_feature):
    try:
        vectorizer = TfidfVectorizer(max_features=max_feature)
        X_train = vectorizer.fit_transform(train_df['text'].values)
        X_test = vectorizer.transform(test_df['text'].values)

        # Assign feature names to columns
        feature_names = vectorizer.get_feature_names_out()
        train_features = pd.DataFrame(X_train.toarray(), columns=feature_names)
        test_features = pd.DataFrame(X_test.toarray(), columns=feature_names)

        # Add target column back
        if 'target' in train_df.columns:
            train_features['target'] = train_df['target'].values
        if 'target' in test_df.columns:
            test_features['target'] = test_df['target'].values

        return train_features, test_features
    except Exception as e:
        logger.error("Error during feature extraction: %s", str(e))
        return None, None

# Save data to disk
def save_data(train_data, test_data, data_path):
    try:
        logger.debug(f"Saving data to {data_path}")
        data_path = os.path.join(data_path, 'processed')
        os.makedirs(data_path, exist_ok=True)

        train_data.to_csv(os.path.join(data_path, 'tfidf_train_data.csv'), index=False)
        test_data.to_csv(os.path.join(data_path, 'tfidf_test_data.csv'), index=False)

        logger.debug("Data saved successfully.")
    except Exception as e:
        logger.error("Error saving data: %s", str(e))

# Main function
def main():
    train_df = load_data('./data/interim/preprocessed_train_data.csv')
    test_df = load_data('./data/interim/preprocessed_test_data.csv')

    if train_df is not None and test_df is not None:
        logger.debug('Preprocessed data is loaded')
        max_feature=  load_params(file_path='params.yaml')['feature_engineering']['max_feature']
        train_df_tfidf, test_df_tfidf = feature_extraction(train_df, test_df , max_feature)

        if train_df_tfidf is not None and test_df_tfidf is not None:
            logger.debug('Feature extraction is done')
            save_data(train_df_tfidf, test_df_tfidf, './data')
            logger.debug('Vectorized data is saved')
        else:
            logger.error('TF-IDF feature extraction failed')
    else:
        logger.error('Data loading failed')


if __name__ == '__main__':
    main()
