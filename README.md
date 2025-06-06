# 📧 Spam Mail Classifier

A machine learning web application that classifies emails as **Spam** or **Ham** using a trained Random Forest model. The app supports two modes of email input:  
1. **Custom message classification**, where you paste email content  
2. **Live inbox classification** using Gmail authentication via **Google OAuth2**

Built with Flask and modularized with support for ML pipeline management and DVC-based data versioning.

---

## 🚀 Demo Features

-  Classify custom messages as spam or not  
-  Authenticate your Gmail and classify real inbox emails  
-  View results instantly on the web interface  

---

## 🧠 Core Features

-  Preprocessing using NLTK (stopword removal, stemming)  
-  TF-IDF vectorization  
-  Random Forest classifier with class balancing  
-  Clean modular pipeline: ingestion → preprocessing → feature engineering → training → evaluation  
-  OAuth2-based Gmail access  
-  Logging and error handling  
-  Data versioning with DVC

---

## 📁 Project Structure

```bash
SPAM-DETECTION-END-TO-END-PIPELINE-MLOPS/
│
├── app.py                          # Flask app entry point
├── dvc.yaml                        # DVC pipeline config
├── requirements.txt
├── README.md
│
├── models/                         # Trained model and vectorizer (excluded from Git)
│   ├── RandomForest.joblib
│   └── vectorizer.joblib
│
├── logs/                           # Logging output
│
├── templates/                      # HTML templates for Flask
│   ├── index.html
│   ├── custom.html
│   └── inbox.html
│
├── static/                         # Static CSS/JS files
│
├── src/
│   ├── __init__.py
│   ├── logger/                     # Logging configuration
│   │   └── __init__.py
│   │
│   ├── components/                 # ML pipeline components
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── preprocess.py
│   │   ├── feature_engineering.py
│   │   ├── model_trainning.py
│   │   └── evaluation.py
│   │
│   ├── pipeline/                   # Training and prediction pipelines
│   │   ├── __init__.py
│   │   ├── trainning_pipeline.py
│   │   └── prediction_pipeline.py
│   │
│   └── utils/
│       └── oauth_gmail.py          # Google OAuth and Gmail integration
        └── main_utils.py
```

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Himanshu0518/Spam-detection-End-to-End-pipeline-MLOPS.git
cd Spam-detection-End-to-End-pipeline-MLOPS
code .  # Open in VS Code (optional)
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Training Pipeline

```bash
python src/pipeline/trainning_pipeline.py
```

This will save the trained model and vectorizer into the `models/` directory.

### 5. Run the Web App

```bash
python app.py
```

Then open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔐 Gmail Inbox Classification (OAuth2)

To classify real emails from your Gmail inbox:

1. On the homepage, select **"Classify from Inbox"**
2. Sign in with your Gmail account (OAuth2 flow)
3. Enter how many emails to classify (up to 50)
4. View spam/ham predictions for each message

> ⚠️ Note: Google may block access if the OAuth app is unverified. To test, add your email as a test user in Google Cloud Console.

---

## 📦 Data Versioning with DVC

This project uses DVC for managing data and model versions.

```bash
dvc init
dvc add data/
dvc add models/
git add dvc.yaml data.dvc models.dvc
git commit -m "Add DVC tracking"
```

---

## 🔍 Model Details

- **Vectorizer**: TF-IDF  
- **Classifier**: Random Forest (class_weight='balanced')  
- **Evaluation Metrics**: Accuracy, Precision, Recall  

---

## 🌐 Web Interface Overview

| Input Type | Description                         |
|------------|-------------------------------------|
| Custom     | Paste your own message/email text   |
| Inbox      | Fetch recent emails from Gmail inbox |

---

## 📌 Future Improvements

- Add more classifiers (e.g., Naive Bayes, XGBoost)  
- Add full email body parsing (not just snippet + subject)  
- Dockerize for easier deployment  
- Deploy to Render / AWS / Heroku  
- Add historical spam statistics per user  

---

## 👨‍💻 Author

**Himanshu Singh**  
GitHub: [@Himanshu0518](https://github.com/Himanshu0518)