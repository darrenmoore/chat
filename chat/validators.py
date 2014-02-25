import re

def email_validator(value):
   email = re.compile(r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)',re.IGNORECASE)
   return bool(email.match(value))

def channel_name_validator(value):
   email = re.compile(r'^\#[-a-z0-9_.]+',re.IGNORECASE)
   return bool(email.match(value))

def password_validator(value):
   return True

def alias_validator(value):
   return True
