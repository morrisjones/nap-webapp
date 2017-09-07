import os
from smtplib import SMTP

#
# Email sent to confirm a reservation request
#
confirm_email_message = """From: D23 North American Pairs <nap@bridgemojo.com>
To: {email}
Subject: Confirm your NAP playoff registration

Hi! You have requested a seat at the NAP semi-final game.

Game: {long_game}
Players: {player_a} and {player_b}
Flight: {long_flight}

To confirm your reservation, please click this link:

https://nap.bridgemojo.com/registration/confirm?key={confirm_key}

Best regards,
District 23 North American Pairs
https://nap.bridgemojo.com
"""


def confirm_email(confirm_key,fields):
  mailhost = os.environ['MAIL_HOST']
  mailuser = os.environ['MAIL_USER']
  mailpass = os.environ['MAIL_PASSWORD']
  fields['confirm_key'] = confirm_key
  body = confirm_email_message.format(**fields)
  email_to = [fields['email']]
  email_from = 'nap@bridgemojo.com'

  smtp = SMTP(mailhost)
  smtp.starttls()
  smtp.login(mailuser,mailpass)
  smtp.sendmail(email_from,email_to,body)

  return