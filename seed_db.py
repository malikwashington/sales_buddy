"""Script to seed database."""

'''api goes in this file'''

import crud
import model
import server
from contact_ops import set_priority

import os
import json
from datetime import datetime

os.system("dropdb salesbuddy --if-exists")
os.system("createdb salesbuddy")

with server.app.app_context():
  model.connect_to_db(server.app)
  model.db.create_all()

  #create user
  test_user = crud.create_user('test','user', 'test@test.com', 'test')

  model.db.session.add(test_user)
  model.db.session.commit()

  # test_user2 = crud.create_user('test2@test.com', 'test')

  # model.db.session.add(test_user2)
  # model.db.session.commit()

  # Load  data from JSON file
  with open("data/MOCK_CONTACT_DATA.json") as f:
      contact_data = json.loads(f.read())

  for contact in contact_data: 
    test_contact = crud.add_contact_to_user(test_user, contact['f_name'], contact['l_name'], contact['urgency'],
                            contact['potential'], contact['opportunity'])
    model.db.session.add(test_contact)
    model.db.session.commit()
  for user_contact in model.User.query.get(1).contacts:
    set_priority(user_contact)
    model.db.session.add(user_contact)
    model.db.session.commit()
