import os
from src.logger import logging
import json
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import yaml 
<<<<<<< HEAD
from src.utils.main_utils import load_data
=======

# Load vectorized test data
def load_data(file_path):
    try:
        logging.debug(f"Loading test data from {file_path}")
        data = pd.read_csv(file_path)
        logging.debug(f"Data loaded. Shape: {data.shape}")
        return data
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        return None
>>>>>>> da1bad4c84c7f59dc82aa1bf26d2871647579b08

# Load model
def load_model(model_path):
    try:
        logging.debug(f"Loading model from {model_path}")
        model = joblib.load(model_path)
        logging.debug("Model loaded successfully")
        return model
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")
        return None

# Evaluate model
def evaluate_model(model, test_df):
    try:
        X_test = test_df.drop(columns=['target'])
        y_true = test_df['target']

        y_pred = model.predict(X_test)

        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0)
        }

        logging.debug(f"Evaluation metrics: {metrics}")
        return metrics

    except Exception as e:
        logging.error(f"Error during evaluation: {str(e)}")
        return None

# Save metrics
def save_metrics(metrics, report_path):
    try:
        os.makedirs(report_path, exist_ok=True)
        with open(os.path.join(report_path, 'metrics.json'), 'w') as f:
            json.dump(metrics, f, indent=4)
        logging.debug("Metrics saved to metrics.json")
    except Exception as e:
        logging.error(f"Error saving metrics: {str(e)}")

def load_params(file_path='params.yaml'):
    try:
        with open(file_path, 'r') as f:
            params = yaml.safe_load(f)
        return params
    except Exception as e:
        print(f"Error loading parameters from {file_path}: {e}")
        return None
 
def main():
    test_df = load_data('./data/processed/tfidf_test_data.csv')
    model = load_model('./models/Randomforest.joblib')

    if test_df is not None and model is not None:
        metrics = evaluate_model(model, test_df)
        if metrics is not None:
            save_metrics(metrics, './report')
        else:
            logging.error("Failed to evaluate model")
    else:
        logging.error("Model or test data not loaded")
    

if __name__ == '__main__':
    main()
