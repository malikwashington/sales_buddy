import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_PASSWORD = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_USERNAME = os.getenv('TWILIO_ACCOUNT_SID')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')