import os
import pandas as pd
from src.logger import logging
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
import yaml 
from src.utils.main_utils import load_data

def load_params(file_path='params.yaml'):
    try:
        with open(file_path, 'r') as f:
            params = yaml.safe_load(f)
        return params
    except Exception as e:
        print(f"Error loading parameters from {file_path}: {e}")
        return None
 
def train_model(train_df, model_tuple):
    try:
        logging.debug(f"Training the model: {model_tuple[0]}")
        classifier = model_tuple[1]

        X_train = train_df.drop('target', axis=1)
        y_train = train_df['target']

        classifier.fit(X_train, y_train)
        logging.debug("Model trained successfully.")
        return classifier

    except Exception as e:
        logging.error(f"Error during model training: {str(e)}")
        return None

def save_model(model_name, classifier):
    try:
        model_dir = './models'
        os.makedirs(model_dir, exist_ok=True)

        model_path = os.path.join(model_dir, f'{model_name}.joblib')
        logging.debug(f"Saving model '{model_name}' to {model_path}")

        dump(classifier, model_path)

        logging.info(f"Model saved successfully at {model_path}")
    except Exception as e:
        logging.error(f"Unable to save model '{model_name}': {str(e)}")
        
def main():
    try:
        params = load_params(file_path='params.yaml')['model_trainning']

        model = ('RandomForest', RandomForestClassifier(**params))

        train_df = load_data('./data/processed/tfidf_train_data.csv')
        test_df = load_data('./data/processed/tfidf_test_data.csv')

        if train_df is None or test_df is None:
            logging.error("Data loading failed. Exiting pipeline.")
            return

        classifier = train_model(train_df, model)

        if classifier:
            save_model(model[0], classifier)

    except Exception as e:
        logging.error(f"Unexpected error in main: {str(e)}")

if __name__ == '__main__':
    main()
