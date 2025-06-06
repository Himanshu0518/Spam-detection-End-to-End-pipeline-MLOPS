import os
import pandas as pd
import logging
from sklearn.model_selection import train_test_split
from src.logger import logging
from src.utils.main_utils import load_data

# Clean data
def preprocess(df):
    try:
        df.dropna(inplace=True)
        logging.debug("Dropped null values.")
        df.drop_duplicates(inplace=True)
        logging.debug("Dropped duplicates.")
        return df
    except Exception as e:
        logging.error(f"Error preprocessing data: {str(e)}")

# Save the train/test split
def save_data(train_data, test_data, data_path):
    try:
        logging.debug(f"Saving data to {data_path}")
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)  # FIXED typo: exist_Ok -> exist_ok

        train_data.to_csv(os.path.join(raw_data_path, 'train_data.csv'), index=False)  # ADDED .csv extension
        test_data.to_csv(os.path.join(raw_data_path, 'test_data.csv'), index=False)
        logging.debug("Data saved successfully.")
    except Exception as e:
        logging.error(f"Error saving data: {str(e)}")  # FIXED error: was passing `str(e)` as a second arg

# Main workflow
def main():
    try:
        url = 'https://raw.githubusercontent.com/Himanshu0518/Assets/main/email.csv'
        df = load_data(url)
        if df is not None:
            df_final = preprocess(df)
            train_df, test_df = train_test_split(df_final, test_size=0.2, random_state=20)
            save_data(train_df, test_df, './data')  # CHANGED '/data' to './data' to ensure relative path works
    except Exception as e:
        logging.error(f"Unexpected error in main(): {str(e)}")

# Run the main function
if __name__ == "__main__":
    main()
