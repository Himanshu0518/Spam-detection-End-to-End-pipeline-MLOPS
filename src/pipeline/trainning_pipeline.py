# training_pipeline.py

from src.components import data_ingestion
from src.components import preprocess
from src.components import feature_engineering
from src.components import model_training
from src.components import Evaluation
from src.logger import logging

def main():
    try:
        logging.info("Starting Training Pipeline")

        logging.info("Step 1: Data Ingestion")
        data_ingestion.main()

        logging.info("Step 2: Preprocessing")
        preprocess.main()

        logging.info("Step 3: Feature Engineering")
        feature_engineering.main()

        logging.info("Step 4: Model Training")
        model_training.main()

        logging.info("Step 5: Model Evaluation")
        Evaluation.main()

        logging.info("Training Pipeline Completed Successfully")

    except Exception as e:
        logging.error(f"Error in training pipeline: {str(e)}")


if __name__ == "__main__":
    main()
