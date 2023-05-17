"""Server for sales buddy app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
  """View homepage."""

  return render_template('homepage.html')

@app.route('/signup', methods=['GET','POST'])
def sign_up():
  """sign up page."""
  error = ''
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    user = crud.get_user_by_email(email)
    if user:
      error = 'User already exists'
      return render_template('signup.html', error=error)
    elif password != password2:
      error = 'Passwords do not match'
      return render_template('signup.html', error=error)
    else:
      crud.create_user(email, password)
      flash('Account created! Please log in.')
      return redirect('/homepage')
  return render_template('signup.html')

  
  
if __name__ == '__main__':
  connect_to_db(app)
  app.run(host='0.0.0.0', debug=True)