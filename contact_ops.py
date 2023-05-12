from datetime import datetime
import queue

def set_priority(contact):
  '''defines the priority of a contact based on the urgency, potential, and opportunity scores'''

  p =(contact.urgency+contact.potential+contact.opportunity)/(1+(datetime.utcnow()-contact.last_contacted).days)
  contact.priority = p
  return p

def update_last_contacted(contact):
  '''updates the last_contacted column of a contact to the current time'''
  contact.last_contacted = datetime.utcnow()
  set_priority(contact)
  
def priority_queue(user):
  '''returns a list of contacts for a user sorted by priority'''
  q = queue.PriorityQueue()
  for contact in user.contacts:
    q.put((contact.priority, contact))
