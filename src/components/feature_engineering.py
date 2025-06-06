import os 
import pandas as pd 
from src.logger import logging 
from sklearn.feature_extraction.text import TfidfVectorizer
import yaml
import joblib 
<<<<<<< HEAD
from src.utils.main_utils import load_data
=======

>>>>>>> da1bad4c84c7f59dc82aa1bf26d2871647579b08

def load_params(file_path='params.yaml'):
    try:
        with open(file_path, 'r') as f:
            params = yaml.safe_load(f)
        return params
    except Exception as e:
        print(f"Error loading parameters from {file_path}: {e}")
        return None

<<<<<<< HEAD
=======
# Load preprocessed data
def load_data(file_path):
    try:
        logging.debug(f"Loading data from {file_path}")
        data = pd.read_csv(file_path)
        logging.debug(f"Data loaded successfully. Shape: {data.shape}")
        return data
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        return None
>>>>>>> da1bad4c84c7f59dc82aa1bf26d2871647579b08

# Extract TF-IDF features
def feature_extraction(train_df, test_df,max_feature):
    try:
        vectorizer = TfidfVectorizer(max_features=max_feature)
        X_train = vectorizer.fit_transform(train_df['text'].values)
        X_test = vectorizer.transform(test_df['text'].values)
        
        try:
            model_dir = './models'
            os.makedirs(model_dir, exist_ok=True)

            model_path = os.path.join(model_dir, f'vectorizer.joblib')
            logging.debug(f"Saving TfidfVectorizer in models folder ")

            joblib.dump(vectorizer, model_path)

            logging.info(f"Model saved successfully at {model_path}")
        except Exception as e:
           logging.error(f"Unable to save vectorizer:' {str(e)}")
   
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
        logging.error("Error during feature extraction: %s", str(e))
        return None, None

# Save data to disk
def save_data(train_data, test_data, data_path):
    try:
        logging.debug(f"Saving data to {data_path}")
        data_path = os.path.join(data_path, 'processed')
        os.makedirs(data_path, exist_ok=True)

        train_data.to_csv(os.path.join(data_path, 'tfidf_train_data.csv'), index=False)
        test_data.to_csv(os.path.join(data_path, 'tfidf_test_data.csv'), index=False)

        logging.debug("Data saved successfully.")
    except Exception as e:
        logging.error("Error saving data: %s", str(e))

# Main function
def main():
    train_df = load_data('./data/interim/preprocessed_train_data.csv')
    test_df = load_data('./data/interim/preprocessed_test_data.csv')

    if train_df is not None and test_df is not None:
        logging.debug('Preprocessed data is loaded')
        params = load_params(file_path='params.yaml')

        if params and 'feature_engineering' in params and 'max_feature' in params['feature_engineering']:
            max_feature = params['feature_engineering']['max_feature']
        else:
            raise ValueError("Missing 'feature_engineering.max_feature' in params.yaml")

        train_df_tfidf, test_df_tfidf = feature_extraction(train_df, test_df , max_feature)

        if train_df_tfidf is not None and test_df_tfidf is not None:
            logging.debug('Feature extraction is done')
            save_data(train_df_tfidf, test_df_tfidf, './data')
            logging.debug('Vectorized data is saved')
        else:
            logging.error('TF-IDF feature extraction failed')
    else:
        logging.error('Data loading failed')


if __name__ == '__main__':
    main()
