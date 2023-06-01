from twilio.rest import Client
import keys
from model import db, Call_Record, Text_Record


client = Client(keys.TWILIO_USERNAME, keys.TWILIO_PASSWORD)


  
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


def call_phone(contact, notes):
    '''make a call to a user's phone number needs a country code and to be a string'''

    call = client.calls.create(
        url='http://demo.twilio.com/docs/voice.xml',
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
