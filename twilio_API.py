from twilio.rest import Client
import keys
from model import db, Call_Record, Text_Record
from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.twiml.messaging_response import MessagingResponse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from flask import jsonify


client = Client(keys.TWILIO_USERNAME, keys.TWILIO_PASSWORD)


def token():
  """Generate a Twilio token for a user"""

  token = AccessToken(
                    keys.TWILIO_USERNAME, 
                    keys.TWILIO_API_USERNAME, 
                    keys.TWILIO_API_PASSWORD, 
                    identity='Salesforce User')

  voice_grant = VoiceGrant(
                          outgoing_application_sid=keys.TWIML_APP_SID,
                          incoming_allow=True)
  
  token.add_grant(voice_grant)
  token = token.to_jwt()#.decode('utf-8') not used in twilio docs

  return jsonify(identity='Salesforce User', token=token)

  
def send_sms(contact, text):
  """Send an SMS to a user's contact"""

  prefix = '+1'

  message = client.messages.create(
      to=prefix + contact.phone,
      from_='+18559126913',
      body=text)
  print(message.sid)

  contact.text_history.append(Text_Record(
                              text_body=text,
                              text_time=message.date_sent,
                              from_=message.from_))
  contact.last_contacted = message.date_sent
  db.sesion.add(contact.text_history)
  db.session.commit()

def voice(phone_number):
  """Make a call to a user's contact"""

  resp = VoiceResponse()
  dial = Dial(
            caller_id='+18559126913',
            number=phone_number,
            
            # action='/handleDialCallStatus',
            # method='POST',
            # record='record-from-answer-dual',
            # recording_status_callback_event='in-progress completed',
            # recording_status_callback='https://myapp.com/recording-handler',
            # recording_status_callback_method='POST',
  )

  resp.append(dial)
  
  return str(resp)


def bot_call(contact, notes):
  '''make a call to a contact's phone number using programmable voice api
      needs a country code and to be a string'''

  call = client.calls.create(
      url='https://handler.twilio.com/twiml/EHe938eb74859553c7722a6c0f731e7fb3',
      # instead of url, use twiml
      # twiml='<Response><Connect><Stream url='wss:'>SOMETHING GOES HERE</Stream></Connect></Response>',
      to=contact.phone,
      from_='+19177372192')

  print(call.sid)

  contact.call_history.append(Call_Record(
                              call_time=call.date_created,
                              from_=call.from_,
                              call_notes=notes))

  db.session.add(contact.call_history)
  db.session.commit()
