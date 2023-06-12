"""Server for sales buddy app."""

import forms
import twilio_API
import os
import re
from dotenv import load_dotenv
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
from keys import SECRET_KEY
from flask import Flask, Response, render_template, request, flash, session, redirect, url_for, jsonify
from model import connect_to_db, db, User, Contact
import user_funcs
from jinja2 import StrictUndefined
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import flask_sockets 
import json
import base64
import logging
from contact_funcs import get_calls_by_contact, get_emails_by_contact, get_texts_by_contact, edit_contact, delete_contact, edit_contact_notes 

#this codeblock is to bypass a bug in flask_sockets where it doesn't recognize the route as a websocket 
def add_url_rule(self, rule, _, f, **options):
  """Add a URL rule for websocket handling."""
  self.url_map.add(flask_sockets.Rule(rule, endpoint=f, websocket=True))

flask_sockets.Sockets.add_url_rule = add_url_rule
  

app = Flask(__name__)
sockets = flask_sockets.Sockets(app)
app.jinja_env.undefined = StrictUndefined
app.config['SECRET_KEY'] = SECRET_KEY


phone_pattern = re.compile(r"^[\d\+\-\(\) ]+$")
alphanumeric_only = re.compile("[\W_]+")

load_dotenv()
twilio_number = os.environ.get("TWILIO_CALLER_ID")

# Store the most recently created identity in memory for routing calls
IDENTITY = {"identity": ""}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'homepage'

@app.login_manager.unauthorized_handler
def unauthorized():
  """Redirect unauthorized users to Login page."""
  flash('Sign up or Login to view that page.', 'danger')
  return redirect('/')

@login_manager.user_loader
def load_user(user_id):
  '''Load user by id'''
  return User.query.get(int(user_id))

#Logout
@app.route('/logout')
@login_required
def logout():
  """Log out user."""

  logout_user()
  flash('Logged out successfully.', 'success')
  return redirect('/')

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
  """Custom 404 page."""
  return render_template('404.html'), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
  """Custom 404 page."""
  return render_template('500.html'), 500

#Homepage
@app.route('/', methods=['GET','POST'])
def homepage():
  """View homepage."""
  if current_user.is_authenticated:
    return redirect(url_for('profile'))
  
  form = forms.SignInForm()
  #validate sign in form
  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data
    form.email.data = ''
    form.password.data = ''
    # sign in user
    user = user_funcs.login_user(email, password)

    if user[0]:
      #login user
      login_user(user[1])
      return redirect(url_for('profile')) #send to profile page on login
    else:
      #flash message if incorrect email or password
      flash(f'Incorrect email or password', 'danger')
      return redirect('/')
  elif form.errors: 
    flash(f'Incorrect email or password', 'danger')
    return redirect('/')
  return render_template('homepage.html', form=form)

    
#signup up page
@app.route('/signup', methods=['GET','POST'])
def sign_up():
  """sign up page."""
  
  form = forms.RegistrationForm()  
  
 #validate sign up form 
  if form.validate_on_submit():
    fname = form.fname.data
    lname = form.lname.data
    email = form.email.data
    password = form.password.data
    password2 = form.password2.data
    form.fname.data = ''
    form.lname.data = ''
    form.email.data = ''
    form.password.data = ''
    form.password2.data = ''
    #check if user exists
    if user_funcs.get_user_by_email(email):
      flash(f'Account already exists for {email}!', 'danger')
      return render_template('/signup.html', form=form)
    else:
    #create user 
      user = user_funcs.create_user(fname, lname, email, password)
      db.session.add(user)
      db.session.commit()
      flash(f'Account created for {user.full_name}!', 'success')
      return redirect('/')
  #if form is not valid flash errors
  if form.errors: 
    print(form.errors.values())
    [flash(f'{error[0]}', 'danger') for error in form.errors.values()]
    return render_template('signup.html', form=form)
  return render_template('signup.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
  '''change password page'''
  
  form = forms.ChangePasswordForm()
  if form.validate_on_submit():
    old_password = form.old_password.data
    new_password = form.new_password.data
    new_password2 = form.new_password2.data
    form.old_password.data = ''
    form.new_password.data = ''
    form.new_password2.data = ''
    if current_user.verify_password(old_password):
      current_user.password = new_password
      db.session.commit()
      flash('Password changed successfully', 'success')
      return redirect('/profile')
    else:
      flash('Incorrect password', 'danger')
      return redirect('/change_password')
  return render_template('change_password.html', form=form)

@app.route('/profile')
@login_required
def profile():
  '''profile page'''

  return render_template('profile.html', form=forms.ChangePasswordForm())

@app.route('/dashboard')
@login_required
def dashboard():
  '''dashboard  page'''
  return render_template('dashboard.html')

@app.route('/contacts')
@login_required
def contacts():
  '''contacts page'''
  
  form = forms.ContactForm()
  contacts = user_funcs.get_contacts_by_user(current_user.id)
  contacts = [{
    'contact_id': contact.contact_id, 
    'f_name': contact.f_name, 
    'l_name': contact.l_name, 
    'phone': contact.phone, 
    'email': contact.email, 
    'company': contact.company, 
    'last_contacted': contact.last_contacted, 
    'priority': contact.priority} for contact in contacts]
  return render_template('contacts.html', form=form, contacts=contacts)

@app.route('/contacts/<contact_id>')
@login_required
def contact(contact_id):
  '''returns a single contact'''
    
  contact = user_funcs.get_contact_by_id(current_user.id, contact_id)
  calls = get_calls_by_contact(contact_id)
  calls = [{'call_notes': call.call_notes, 'call_time': call.call_time, 'to': call.to} for call in calls]
  texts = get_texts_by_contact(contact_id)
  texts = [{'text_body': text.text_body, 'text_time': text.text_time, 'to': text.to} for text in texts]
  emails = get_emails_by_contact(contact_id)
  emails = [{'email_body': email.email_body, 'email_time': email.email_time, 'to': email.to} for email in emails]

  contact_dict = {
    'contact_id': contact.contact_id,
    'f_name': contact.f_name,
    'l_name': contact.l_name,
    'phone': contact.phone,
    'linkedin': contact.linkedin,
    'email': contact.email,
    'company': contact.company,
    'notes': contact.notes,
    'urgency': contact.urgency,
    'potential': contact.potential,
    'opportunity': contact.opportunity,
    'last_contacted': contact.last_contacted,
    'priority': contact.priority,
    'call_history': calls,
    'text_history': texts,
    'email_history': emails,
  }
  return contact_dict

@app.route('/contacts/new', methods=['POST'])
@login_required
def new_contact():
  '''new contact route'''

  form = forms.ContactForm(request.form)
  if form.validate_on_submit():
    f_name = form.f_name.data
    l_name = form.l_name.data
    phone = form.phone.data
    linkedin = form.linkedin.data
    email = form.email.data
    company = form.company.data
    notes = form.notes.data
    urgency = form.urgency.data
    potential = form.potential.data
    opportunity = form.opportunity.data
    form.f_name.data = ''
    form.l_name.data = ''
    form.phone.data = ''
    form.linkedin.data = ''
    form.email.data = ''
    form.company.data = ''
    form.notes.data = ''
    form.urgency.data = ''
    form.potential.data = ''
    form.opportunity.data = ''
    contact = user_funcs.add_contact_to_user(
      current_user, 
      f_name, 
      l_name, 
      urgency, 
      potential, 
      opportunity, 
      phone, 
      email,
      company, 
      notes,
      linkedin 
      )
    db.session.add(contact)
    db.session.commit()
    flash(f'Contact created for {contact.full_name}!', 'success')
    return redirect('/contacts')

@app.route('/contacts/<contact_id>/edit', methods=['GET','POST'])
@login_required
def edit_existing_contact(contact_id):
  '''edit contact route'''

  if request.method == 'GET':
    return render_template('404.html')
  
  # form = request.form
  form = forms.ContactForm(request.form)

  #validate the form
  if form.validate_on_submit():
    #edit contact
    full_name = f'{form.f_name.data} {form.l_name.data}'
    
    f_name = form.f_name.data
    l_name = form.l_name.data
    phone = form.phone.data
    linkedin = form.linkedin.data
    email = form.email.data
    company = form.company.data
    notes = form.notes.data
    urgency = form.urgency.data
    potential = form.potential.data
    opportunity = form.opportunity.data

    edit_contact(current_user.id ,contact_id, f_name, l_name, phone, linkedin, email, company, notes, urgency, potential, opportunity)
    flash(f'Contact {full_name} edited!', 'success')
    return redirect('/contacts')
  else :
    flash(f'Contact not edited!', 'danger')
    return render_template('contacts.html', form=form)


@app.route('/contacts/<contact_id>/edit/notes', methods=['POST'])
@login_required
def edit_existing_contact_notes(contact_id):
  '''edit contact notes route'''
  if request.method == 'GET':
    return render_template('404.html')
  form = request.form
  contact = user_funcs.get_contact_by_id(current_user.id, contact_id)
  notes = form.get('notes').strip()
  
  flash(f'Contact {contact.full_name} edited!', 'success')
  edit_contact_notes(current_user.id ,contact_id, notes)
  return redirect('/contacts')

@app.route('/contacts/<contact_id>/delete', methods=['GET','POST'])
@login_required
def delete_existing_contact(contact_id):
  '''delete contact route'''
  
  if request.method == 'GET':
    return render_template('404.html')
  
  
  #delete contact
  full_name = user_funcs.get_contact_by_id(current_user.id, contact_id).full_name
  user_funcs.delete_contact_by_id(current_user.id, contact_id)

  flash(f'Contact {full_name} deleted!', 'success')
  
  return redirect('/contacts')

@app.route('/sequences', methods=['GET','POST'])
@login_required
def sequences():
  '''sequences page'''
  form = forms.SequenceForm()
  return render_template('sequences.html', form=form)
  
@app.route('/contacts/<contact_id>/text', methods=['GET', 'POST'])
@login_required
def text(contact_id):
  '''route to stand as endpoint for text messages'''

  if request.method == 'GET':
    return render_template('404.html')
  
  form = request.form
  contact = user_funcs.get_contact_by_id(current_user.id, contact_id)
  sms = form.get('sms').strip()
  twilio_API.send_sms(contact, sms)
  return redirect('/contacts')

# @app.route('/phone', methods=['GET', 'POST'])
@app.route('/phone')
@login_required
def phone():
  '''route to stand as endpoint to host page for phone calls'''
  # return app.send_static_file('phone.html')
  return render_template('phone.html')


# # @sockets.route('/forwarding')
# # @login_required
# # def phone(ws):
# #   '''creating a websocket route to handle incoming phone calls from twilio api
# #   and route them to my personal phone number using the twilio api'''
  
# #   app.logger.info('Connection accepted')
# #   print('\n\n\n\n\n', ws, '\n\n\n\n\n')
# #   while not ws.closed:
# #     message = ws.receive()
# #     if message is None:
# #       app.logger.info('No message received...')
#       continue
#     message = json.loads(message)
#     print('\n\n', message, '\n\n')
#     if message['type'] == 'call':
#       resp = twilio_API.voice(message['number'])
#       ws.send(resp)
#     elif message['type'] == 'text':
#       resp = twilio_API.send_sms(message['number'], message['text'])
#       ws.send(resp)
#     else:
#       print('error')
#       ws.send('error')
#   print('closed')
#   ws.close()

@app.route("/voice", methods=["POST"])
def voice():
  print('\n\n\n\n\n', 'welcome to the terror dome', '\n\n\n\n\n')
  resp = VoiceResponse()
  if request.form.get("To") == twilio_number:
      # Receiving an incoming call to our Twilio number
      dial = Dial()
      # Route to the most recently created client based on the identity stored in the session
      dial.client(IDENTITY["identity"])
      resp.append(dial)
  elif request.form.get("To"):
      # Placing an outbound call from the Twilio client
      dial = Dial(caller_id=twilio_number)
      # wrap the phone number or client name in the appropriate TwiML verb
      # by checking if the number given has only digits and format symbols
      if phone_pattern.match(request.form["To"]):
          dial.number(request.form["To"])
      else:
          dial.client(request.form["To"])
      resp.append(dial)
  else:
      resp.say("Thanks for calling!")

  return Response(str(resp), mimetype="text/xml")
  

@app.route('/email', methods=['GET', 'POST'])
@login_required
def email():
  '''route to handle emails from twilio api'''

@app.route('/calls', methods=['GET', 'POST'])
@login_required
def calls():
  '''route to handle calls from twilio api'''

  return render_template('calls.html')

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
  '''route to handle tasks list'''
  
  return render_template('tasks.html')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
  '''route to handle admin page'''
  
  if current_user.admin:
    return render_template('admin.html')
  else:
    flash('You do not have access to that page', 'danger')
    return redirect('/profile')
  

@app.route("/token", methods=["GET"])
@login_required
def token():
    '''get twilio token for client'''

    # get credentials for environment variables
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    application_sid = os.environ["TWILIO_TWIML_APP_SID"]
    api_key = os.environ["API_KEY"]
    api_secret = os.environ["API_SECRET"]

    # Generate a random user name and store it
    identity = alphanumeric_only.sub("", current_user.full_name)
    IDENTITY["identity"] = identity

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a Voice grant and add to token
    voice_grant = VoiceGrant(
        outgoing_application_sid=application_sid,
        incoming_allow=True,
    )
    token.add_grant(voice_grant)

    # Return token info as JSON
    token = token.to_jwt()

    # Return token info as JSON
    return jsonify(identity=identity, token=token)

  
if __name__ == '__main__':
  # app.logger.setLevel(logging.DEBUG)
  # from gevent import pywsgi
  # from geventwebsocket.handler import WebSocketHandler
  connect_to_db(app)
  
  # server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
  print('\n\n Server started \n\n')
  # server.serve_forever()
  
 #this is the old way to start the server before flask_sockets was added
  app.run(host='0.0.0.0', debug=True)
 