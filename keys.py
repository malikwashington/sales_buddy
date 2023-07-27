import os
from dotenv import load_dotenv
#this file stores all of my environment variables
load_dotenv()

TWILIO_PASSWORD = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_USERNAME = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_API_USERNAME = os.getenv('TWILIO_API_KEY_SID')
TWILIO_API_PASSWORD = os.getenv('TWILIO_API_KEY_SECRET')
TWIML_APP_SID = os.getenv('TWIML_APP_SID')

EMAIL = os.getenv('GOOGLE_ACCOUNT')
MAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
CAL_PASSWORD = os.getenv("GCAL_PASSWORD")

ADMIN = os.getenv('ADMIN_USERNAME')
ADMIN_KEY  = os.getenv('ADMIN_PASSWORD')

SECRET_KEY = os.getenv('SECRET_KEY')

BOSS = os.getenv('MASTER_NUMBER')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
BIZ_PHONE = os.getenv('BIZ_NUMBER')

CLOUDINARY_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_SECRET = os.getenv('CLOUDINARY_API_SECRET')
CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')