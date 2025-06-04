from flask import Flask, request, render_template
from src.pipeline.prediction_pipeline import SpamClassifier
from src.logger import logging

app = Flask(__name__)
classifier = SpamClassifier()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_result():
    message = request.form.get('message', '')
    if message.strip():  # check if message is not just whitespace
        logging.info(f"Received message: {message}")
        prediction = classifier.predict_single(message)
        return render_template('index.html', prediction=prediction, input_text=message)
    else:
        return render_template('index.html', prediction=None, input_text='')

if __name__ == '__main__':
    app.run(debug=True)
