"""Server for sales buddy app."""

import forms
from keys import SECRET_KEY
from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db, User, Contact
import user_funcs

from jinja2 import StrictUndefined
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'homepage'

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

@app.route('/profile')
@login_required
def profile():
  '''profile page'''
  return render_template('profile.html')
  
if __name__ == '__main__':
  connect_to_db(app)
  app.run(host='0.0.0.0', debug=True)