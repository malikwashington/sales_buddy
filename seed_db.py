"""Script to seed database."""

'''api goes in this file'''


import user_funcs
import contact_funcs
import model
import server
from contact_funcs import set_priority
import os
import json
from datetime import datetime
import re


os.system("dropdb salesbuddy --if-exists")
os.system("createdb salesbuddy")

with server.app.app_context():
    model.connect_to_db(server.app)
    model.db.create_all()

    # create user
    test_user = user_funcs.create_user('test', 'user', 'test@test.com', 'test')

    model.db.session.add(test_user)
    model.db.session.commit()

    # test_user2 = crud.create_user('test2@test.com', 'test')

    # model.db.session.add(test_user2)
    # model.db.session.commit()

    # Load  data from JSON file
    with open("data/Mock3.json") as f:
        contact_data = json.loads(f.read())
        
    for contact in contact_data:
        test_contact = user_funcs.add_contact_to_user(
            test_user, contact['f_name'], contact['l_name'],
            contact['urgency'], contact['potential'],
            contact['opportunity'], contact['phone'],
            contact['email'],contact['company'], contact['notes'])
        print('\n\n\n\n\n\n\n\n\last_contacted: ', test_contact.last_contacted,'\n\n\n\n\n\n\n')

        for i, record in enumerate(contact['call_history']):
            record['call_time'] = re.sub('[:\-]', '', record['call_time'].strip())
            record['call_time'] = re.sub('\s', ',', record['call_time'])
            
            # if test_contact.last_contacted == None:
            #     test_contact.last_contacted = record['call_time']
            #     print('\n\n\n\n\n\n\n\n\last_contacted: ', test_contact.last_contacted,'\n\n\n\n\n\n\n')
            # elif record['call_time'] > contact.last_contacted:
            #     test_contact.last_contacted = record['call_time']
            #     print('\n\n\n\n\n\n\n\n\last_contacted: ', test_contact.last_contacted,'\n\n\n\n\n\n\n')
                
            test_contact = contact_funcs.add_call_to_contact(
                test_contact, record['call_notes'], record['call_time'])

        for i, record in enumerate(contact['text_history']):
            record['text_time'] = re.sub('[:\-]', '', record['text_time'].strip())
            record['text_time'] = re.sub('\s', ',', record['text_time'])

            # if test_contact['last_contacted'] == None:
            #     test_contact.last_contacted = record['text_time']
            # elif record['text_time'] > test_contact.last_contacted:
            #     test_contact['last_contacted'] = record['text_time']
            
            test_contact = contact_funcs.add_text_to_contact(
                test_contact, record['text_body'], record['text_time'])

        for i, record in enumerate(contact['email_history']):
            record['email_time'] = re.sub('[:\-]', '', record['email_time'].strip())
            record['email_time'] = re.sub('\s', ',', record['email_time'])

            # if test_contact['last_contacted'] == None:
            #     test_contact['last_contacted'] = record['email_time']
            # elif record['email_time'] > test_contact.last_contacted:
            #     test_contact['last_contacted'] = record['email_time']

            test_contact = contact_funcs.add_email_to_contact(
                test_contact, record['email_body'], record['email_time'])

        model.db.session.add(test_contact)
        model.db.session.commit()

    for user_contact in model.User.query.get(1).contacts:
        set_priority(user_contact)

        model.db.session.add(user_contact)
        model.db.session.commit()
