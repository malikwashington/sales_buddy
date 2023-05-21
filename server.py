"""Server for sales buddy app."""

from forms import RegistrationForm
from keys import SECRET_KEY
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined
# from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import RegistrationForm

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config['SECRET_KEY'] = SECRET_KEY

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
@app.route('/')
def homepage():
  """View homepage."""

  return render_template('homepage.html')

#signup up page
@app.route('/signup', methods=['GET','POST'])
def sign_up():
  """sign up page."""
  
  form = RegistrationForm()  
  name = None
  
  if form.validate_on_submit():
    fname = form.fname.data
    lname = form.lname.data
    email = form.email.data
    password = form.password.data
    form.fname.data = ''
    form.lname.data = ''
    form.email.data = ''
    form.password.data = ''
    form.password2.data = ''
    if crud.get_user_by_email(email):
      flash(f'Account already exists for {form.email.data}!', 'danger')
      return redirect('/signup')
    else:
      user = crud.create_user(fname, lname, email, password)
      db.session.add(user)
      db.session.commit()
      flash(f'Account created for {form.name.data}!', 'success')
      return redirect('/')
  
  return render_template('signup.html', form=form, name=name)

  
  
if __name__ == '__main__':
  connect_to_db(app)
  app.run(host='0.0.0.0', debug=True)