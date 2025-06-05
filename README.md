# 📧 Spam Mail Classifier

A machine learning web application that classifies emails as **Spam** or **Ham** using a trained Random Forest model and vectorizer. Built using Flask, with modular design and support for data versioning using DVC.

---

## 🚀 Demo

Paste any email content and instantly see whether it's classified as **Spam** or **Ham**.

---

## 🧠 Features

- Preprocessing using NLTK (stopwords removal, stemming)
- Random Forest classification
- TF-IDF vectorization
- Modular ML pipeline (`data_ingestion`, `preprocessing`, `feature_engineering`, `training`, `evaluation`)
- Web interface built using Flask
- Logging for debugging and tracing
- Data versioning with DVC

---

## 📁 Project Structure

SPAM-DETECTION-END-TO-END-PIPELINE-MLOPS/
│
├── app.py # Flask app entry point
├── dvc.yaml # DVC pipeline config
├── requirements.txt
├── README.md
│
├── models/ # Trained model and vectorizer
│ ├── RandomForest.joblib
│ └── vectorizer.joblib
│
├── logs/ # Logs for tracking
│
├── templates/ # HTML templates
│ └── index.html
│
├── src/
│ ├── __init__.py
│ ├── logger/
│ │ └── __init__.py # Logging setup
│ │
│ ├── components/ # Core pipeline components
│ │ ├── __init__.py
│ │ ├── data_ingestion.py
│ │ ├── preprocess.py
│ │ ├── feature_engineering.py
│ │ ├── model_trainning.py
│ │ └── evaluation.py
│ │
│ └── pipeline/ # Pipelines for training and prediction
│ ├── __init__.py
│ ├── trainning_pipeline.py
│ └── prediction_pipeline.py


---

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Himanshu0518/Spam-detection-End-to-End-pipeline-MLOPS.git
   cd Spam-detection-End-to-End-pipeline-MLOPS
   write code . (to enter VS code)

2. Create and Activate Virtual Environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Run Training Pipeline
This step will train the model and save it to the models/ directory.
python src/pipeline/trainning_pipeline.py

5. 🧪 Running Locally
python app.py
Then open your browser and visit: http://127.0.0.1:5000

## 📦 Data Versioning (DVC)
This project uses DVC to version control data and model files.

* Basic DVC commands:

Initialize DVC:
dvc init
 
* Track dataset/model:
dvc add data
dvc add models

git add dvc.yaml
git commit -m "Track dataset and model with DVC"


🔍 Model Overview
* Vectorizer: TF-IDF (Term Frequency–Inverse Document Frequency)
* Classifier: Random Forest (with class balancing)
* Evaluation Metrics: Accuracy, Precision, Recall

🌐 Web Interface
Input: Any email/message text
Output: Spam or Ham displayed on the page

📌 Future Improvements
* Add more classifiers (Naive Bayes, XGBoost)
* Integrate email scraping for live input
* Deploy on cloud platforms (Render, Heroku, AWS)
* Build Docker support


👨‍💻 Author
Himanshu Singh – @Himanshu0518