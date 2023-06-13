import os
from dotenv import load_dotenv
#this file stores all of my environment variables
load_dotenv()

TWILIO_PASSWORD = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_USERNAME = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_API_USERNAME = os.getenv('TWILIO_API_KEY_SID')
TWILIO_API_PASSWORD = os.getenv('TWILIO_API_KEY_SECRET')
TWIML_APP_SID = os.getenv('TWIML_APP_SID')

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

SECRET_KEY = os.getenv('SECRET_KEY')

BOSS = os.getenv('MASTER_NUMBER')
BIZ_PHONE = os.getenv('TWILIO_NUMBER')

CLOUDINARY_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_SECRET = os.getenv('CLOUDINARY_API_SECRET')
CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')