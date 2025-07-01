from flask import Flask, request, render_template, flash
from src.pipeline.prediction_pipeline import SpamClassifier
from src.logger import logging
import os


app = Flask(__name__)
app.secret_key = 'your-super-secret-key' 

classifier = SpamClassifier()

@app.route('/')
def index():
    return render_template('index.html')  # Shows two options: custom or inbox

@app.route('/custom', methods=['GET', 'POST'])
def custom_email():
    prediction = None
    input_text = ""
    if request.method == 'POST':
        input_text = request.form.get('message', '').strip()
        if input_text:
            logging.info(f"Received custom message: {input_text}")
            prediction = classifier.predict_single(input_text)
    return render_template('custom.html', prediction=prediction, input_text=input_text)



if __name__ == '__main__':
    app.run(host = "0.0.0.0",debug=True)
