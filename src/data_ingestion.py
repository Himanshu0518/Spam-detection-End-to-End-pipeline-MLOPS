import os
import pandas as pd
import logging
from sklearn.model_selection import train_test_split

# Setup logging
os.makedirs('./logs', exist_ok=True)

logger = logging.getLogger('data_ingestion')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('./logs/data_ingestion.log')  # Save inside logs folder
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

if not logger.handlers:  # Prevent duplicate handlers on reruns
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# Load CSV data
def load_data(file_path):
    try:
        logger.debug(f"Loading data from {file_path}")
        data = pd.read_csv(file_path)
        logger.debug(f"Data loaded successfully. Shape: {data.shape}")
        return data
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")

# Clean data
def preprocess(df):
    try:
        df.dropna(inplace=True)
        logger.debug("Dropped null values.")
        df.drop_duplicates(inplace=True)
        logger.debug("Dropped duplicates.")
        return df
    except Exception as e:
        logger.error(f"Error preprocessing data: {str(e)}")

# Save the train/test split
def save_data(train_data, test_data, data_path):
    try:
        logger.debug(f"Saving data to {data_path}")
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)  # FIXED typo: exist_Ok -> exist_ok

        train_data.to_csv(os.path.join(raw_data_path, 'train_data.csv'), index=False)  # ADDED .csv extension
        test_data.to_csv(os.path.join(raw_data_path, 'test_data.csv'), index=False)
        logger.debug("Data saved successfully.")
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")  # FIXED error: was passing `str(e)` as a second arg

# Main workflow
def main():
    try:
        url = 'https://raw.githubusercontent.com/Himanshu0518/datasets/main/email.csv'
        df = load_data(url)
        if df is not None:
            df_final = preprocess(df)
            train_df, test_df = train_test_split(df_final, test_size=0.2, random_state=20)
            save_data(train_df, test_df, './data')  # CHANGED '/data' to './data' to ensure relative path works
    except Exception as e:
        logger.error(f"Unexpected error in main(): {str(e)}")

# Run the main function
if __name__ == "__main__":
    main()
