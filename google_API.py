import os.path
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError



SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def connect_to_gmail():
  '''connect to gmail api'''
  
  creds = None
  
  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file(
      'token.json', ['https://www.googleapis.com/auth/gmail.send'])

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        '.credentials.json', ['https://www.googleapis.com/auth/gmail.send'])
      creds = flow.run_local_server(port=0)
    
    with open('token.json', 'w') as token:
      token.write(creds.to_json())
      
  try:
    #call the gmail api
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', []) 
    if not labels:
      print('No labels found.')
      return
    print('Labels:')
    for label in labels:
      print(label['name'])

  except HttpError as error:
    print(F'An error occurred: {error}')



def send_email(contact, subject, text):
  '''send an email to a user's contact'''

  creds, _ = google.auth.default()
  
  try:
    service = build('gmail', 'v1', credentials=creds)
    message = EmailMessage()
    
    message.set_content(text)
    
    message['To'] = contact.email
    message['From'] = 'malikwashingtonmusic@gmail.com'
    message['Subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    create_message = {
      'raw': encoded_message
    }

    send_message = (service.users().messages().send(
                      userId='me', body=create_message).execute())

    print(F'Message Id: {send_message["id"]}')

  except HttpError as error:
    print(F'An error occurred: {error}')
    send_message = None
  return send_message





if __name__ == '__main__':
  '''only run this if this file is run directly'''
  connect_to_gmail()