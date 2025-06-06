from flask import Flask, request, render_template, redirect, session, url_for, flash
from src.pipeline.prediction_pipeline import SpamClassifier
from src.logger import logging
from src.utils.oauth_gmail import start_oauth_flow, finish_oauth_flow, get_gmail_service, is_authenticated
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

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

@app.route('/oauth')
def oauth():
    return start_oauth_flow()

@app.route('/oauth2callback')
def oauth2callback():
    return finish_oauth_flow()

@app.route('/debug/auth')
def debug_auth():
    """Debug route to check authentication status"""
    auth_status = is_authenticated()
    creds_data = session.get('credentials')
    return {
        'authenticated': auth_status,
        'has_credentials': bool(creds_data),
        'credentials_keys': list(creds_data.keys()) if creds_data else None,
        'session_keys': list(session.keys())
    }
@app.route('/inbox', methods=['GET', 'POST'])
def inbox():
    # Check if user is authenticated
    if not is_authenticated():
        flash('Please authenticate your Gmail account first')
        return render_template('inbox.html', show_auth_required=True, authenticated=False)
    
    if request.method == 'POST':
        try:
            # Get number of emails from form data
            num_emails = int(request.form.get('num_emails', 10))
            
            if num_emails < 1 or num_emails > 50:
                flash('Number of emails must be between 1 and 50')
                return render_template('inbox.html', authenticated=True)
            
            service = get_gmail_service()
            if not service:
                flash('Failed to connect to Gmail. Please re-authenticate.')
                return render_template('inbox.html', show_auth_required=True, authenticated=False)

            logging.info(f"Fetching {num_emails} emails from Gmail")
            
            results = service.users().messages().list(userId='me', maxResults=num_emails).execute()
            messages = results.get('messages', [])
            
            if not messages:
                flash('No emails found in your inbox')
                return render_template('inbox.html', emails={}, num_emails=num_emails, authenticated=True)

            email_texts = {}
            processed_count = 0
            
            for msg in messages:
                try:
                    msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
                    snippet = msg_detail.get('snippet', '')
                    
                    headers = msg_detail.get('payload', {}).get('headers', [])
                    subject = ''
                    for header in headers:
                        if header['name'] == 'Subject':
                            subject = header['value']
                            break
                    
                    email_content = f"{subject} {snippet}".strip()
                    
                    if email_content:
                        prediction = classifier.predict_single(email_content)
                        label = "Spam" if int(prediction) == 1 else "Not Spam"
                        email_texts[email_content] = label
                        processed_count += 1
                        
                except Exception as e:
                    logging.error(f"Error processing message {msg['id']}: {str(e)}")
                    continue
            
            logging.info(f"Successfully processed {processed_count} emails")
            print(f"Email results: {email_texts}")
            
            if processed_count > 0:
                flash(f'Successfully analyzed {processed_count} emails')
            else:
                flash('No emails could be processed')
            
            return render_template('inbox.html', emails=email_texts, num_emails=num_emails, authenticated=True)
            
        except Exception as e:
            logging.error(f"Error in inbox route: {str(e)}")
            flash(f'Error fetching emails: {str(e)}')
            return render_template('inbox.html', authenticated=is_authenticated())
    
    else:
        return render_template('inbox.html', authenticated=is_authenticated())


if __name__ == '__main__':
    app.run(debug=True)