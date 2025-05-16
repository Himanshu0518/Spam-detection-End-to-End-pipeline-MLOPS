import os
import pandas as pd
import logging
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
import yaml 

# Setup logging
os.makedirs('./logs', exist_ok=True)

logger = logging.getLogger('model_training')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('./logs/model_training.log')
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
 
def load_data(file_path):
    try:
        logger.debug(f"Loading data from {file_path}")
        data = pd.read_csv(file_path)
        logger.debug(f"Data loaded successfully. Shape: {data.shape}")
        return data
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return None

def train_model(train_df, model_tuple):
    try:
        logger.debug(f"Training the model: {model_tuple[0]}")
        classifier = model_tuple[1]

        X_train = train_df.drop('target', axis=1)
        y_train = train_df['target']

        classifier.fit(X_train, y_train)
        logger.debug("Model trained successfully.")
        return classifier

    except Exception as e:
        logger.error(f"Error during model training: {str(e)}")
        return None

def save_model(model_name, classifier):
    try:
        model_dir = './models'
        os.makedirs(model_dir, exist_ok=True)

        model_path = os.path.join(model_dir, f'{model_name}.joblib')
        logger.debug(f"Saving model '{model_name}' to {model_path}")

        dump(classifier, model_path)

        logger.info(f"Model saved successfully at {model_path}")
    except Exception as e:
        logger.error(f"Unable to save model '{model_name}': {str(e)}")
        
def main():
    try:
        params = load_params(file_path='params.yaml')['model_trainning']

        model = ('RandomForest', RandomForestClassifier(**params))

        train_df = load_data('./data/processed/tfidf_train_data.csv')
        test_df = load_data('./data/processed/tfidf_test_data.csv')

        if train_df is None or test_df is None:
            logger.error("Data loading failed. Exiting pipeline.")
            return

        classifier = train_model(train_df, model)

        if classifier:
            save_model(model[0], classifier)

    except Exception as e:
        logger.error(f"Unexpected error in main: {str(e)}")

if __name__ == '__main__':
    main()
