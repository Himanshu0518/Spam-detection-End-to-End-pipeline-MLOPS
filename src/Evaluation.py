import os
import logging
import json
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from dvclive import Live
import yaml 

# Setup logging
os.makedirs('./logs', exist_ok=True)

logger = logging.getLogger('model_evaluation')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('./logs/evaluation.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# Load vectorized test data
def load_data(file_path):
    try:
        logger.debug(f"Loading test data from {file_path}")
        data = pd.read_csv(file_path)
        logger.debug(f"Data loaded. Shape: {data.shape}")
        return data
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return None

# Load model
def load_model(model_path):
    try:
        logger.debug(f"Loading model from {model_path}")
        model = joblib.load(model_path)
        logger.debug("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
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

        logger.debug(f"Evaluation metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error during evaluation: {str(e)}")
        return None

# Save metrics
def save_metrics(metrics, report_path):
    try:
        os.makedirs(report_path, exist_ok=True)
        with open(os.path.join(report_path, 'metrics.json'), 'w') as f:
            json.dump(metrics, f, indent=4)
        logger.debug("Metrics saved to metrics.json")
    except Exception as e:
        logger.error(f"Error saving metrics: {str(e)}")

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
            logger.error("Failed to evaluate model")
    else:
        logger.error("Model or test data not loaded")
    
    with Live(save_dvc_exp = True) as live:
        live.log_metric('accuracy',metrics['accuracy'])
        live.log_metric( 'precision',metrics[ 'precision'])
        live.log_metric('recall',metrics['recall'])
        live.log_params(load_params(file_path='params.yaml'))

if __name__ == '__main__':
    main()
