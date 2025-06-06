from src.logger import logging
import pandas as pd 

def load_data(file_path):
    try:
        logging.debug(f"Loading data from {file_path}")
        data = pd.read_csv(file_path)
        logging.debug(f"Data loaded successfully. Shape: {data.shape}")
        return data
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
