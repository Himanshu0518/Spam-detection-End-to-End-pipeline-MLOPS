from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from flask import session, redirect, url_for, request, flash
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def start_oauth_flow():
    try:
        # Check if credentials.json exists
        if not os.path.exists('credentials.json'):
            flash('Gmail credentials file not found. Please add credentials.json file.')
            return redirect(url_for('index'))
        
        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes=SCOPES,
            redirect_uri='http://localhost:5000/oauth2callback'
        )

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'  # force refresh_token even on repeat logins
        )

        # Store the state and redirect URI in session
        session['oauth_state'] = state
        session['redirect_uri'] = flow.redirect_uri
        
        return redirect(authorization_url)
        
    except Exception as e:
        flash(f'Error starting OAuth flow: {str(e)}')
        return redirect(url_for('index'))


def finish_oauth_flow():
    try:
        state = session.get('oauth_state')
        redirect_uri = session.get('redirect_uri')
        
        if not state or not redirect_uri:
            flash('OAuth state not found. Please try authenticating again.')
            return redirect(url_for('inbox'))

        # Verify state parameter to prevent CSRF attacks
        if request.args.get('state') != state:
            flash('Invalid OAuth state. Please try authenticating again.')
            return redirect(url_for('inbox'))

        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes=SCOPES,
            state=state,
            redirect_uri=redirect_uri
        )

        # Handle authorization response
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials

        # Store credentials in session with all necessary fields
        session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

        # Clean up OAuth state from session
        session.pop('oauth_state', None)
        session.pop('redirect_uri', None)

        # Debug print
        print(f"Credentials stored: {bool(session.get('credentials'))}")
        print(f"Session keys: {list(session.keys())}")

        flash('Gmail account authenticated successfully!')
        return redirect(url_for('inbox'))
        
    except Exception as e:
        flash(f'Error completing OAuth flow: {str(e)}')
        return redirect(url_for('inbox'))


def get_gmail_service():
    """Get Gmail service object if user is authenticated"""
    try:
        creds_data = session.get('credentials')
        if not creds_data:
            return None

        creds = Credentials(**creds_data)
        
        # Check if credentials are valid
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                # Try to refresh the token
                try:
                    creds.refresh(Request())
                    # Update session with new credentials
                    session['credentials'] = {
                        'token': creds.token,
                        'refresh_token': creds.refresh_token,
                        'token_uri': creds.token_uri,
                        'client_id': creds.client_id,
                        'client_secret': creds.client_secret,
                        'scopes': creds.scopes
                    }
                except Exception as refresh_error:
                    print(f"Token refresh failed: {refresh_error}")
                    return None
            else:
                return None

        service = build('gmail', 'v1', credentials=creds)
        return service
        
    except Exception as e:
        print(f"Error creating Gmail service: {str(e)}")
        return None


def is_authenticated():
    """Check if user is authenticated with Gmail"""
    creds_data = session.get('credentials')
    print(f"Checking authentication - has credentials: {bool(creds_data)}")
    
    if not creds_data:
        return False
    
    try:
        creds = Credentials(**creds_data)
        is_valid = creds.valid or (creds.expired and creds.refresh_token)
        print(f"Credentials valid: {is_valid}")
        return is_valid
    except Exception as e:
        print(f"Error checking credentials: {e}")
        return False


def clear_credentials():
    """Clear stored credentials from session"""
    session.pop('credentials', None)
    session.pop('oauth_state', None)
    session.pop('redirect_uri', None)