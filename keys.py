import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_PASSWORD = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_USERNAME = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_API_USERNAME = os.getenv('TWILIO_API_KEY_SID')
TWILIO_API_PASSWORD = os.getenv('TWILIO_API_KEY_SECRET')
TWIML_APP_SID = os.getenv('TWIML_APP_SID')

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

SECRET_KEY = os.getenv('SECRET_KEY')