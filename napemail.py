import os
import logging
from smtplib import SMTP

#
# Email sent to confirm a reservation request
#
confirm_email_message = """From: D23 North American Pairs <nap@bridgemojo.com>
To: {email}
Subject: Confirm your NAP playoff registration

Hi! You have requested a seat at the NAP semi-final game.

Game: {game_desc}
Players: {player_a} and {player_b}
Flight: {flight_desc}

To confirm your reservation, please click this link:

{scheme}://{host}/registration/confirm?key={confirm_key}

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

  logging.info("confirm email send to %s" % email_to)
  return

congrats_email = """From: D23 North American Pairs <nap@bridgemojo.com>
To: {email}
Subject: Here is your provisional table assignment

Congratulations! You have reserved a seat at a North American Pairs semi-final (Unit Final) game.

Game: {game_desc}
Players: {player_a} and {player_b}
Flight: {flight_desc}

Your provisional table assignment for the first session is {table_number} {direction}

Please arrive early at the game site with $52 for the session ($13/player per session).

If your plans change, please drop me a note! I'll be happy to change your reservation.
Reply to this message, or write to nap@bridgemojo.com.

Best regards,
District 23 North American Pairs
https://nap.bridgemojo.com
"""

def send_congrats_email(fields):
  mailhost = os.environ['MAIL_HOST']
  mailuser = os.environ['MAIL_USER']
  mailpass = os.environ['MAIL_PASSWORD']
  body = congrats_email.format(**fields)
  email_to = [fields['email']]
  email_from = 'nap@bridgemojo.com'

  smtp = SMTP(mailhost)
  smtp.starttls()
  smtp.login(mailuser,mailpass)
  smtp.sendmail(email_from,email_to,body)

  logging.info("congrats email send to %s" % email_to)
  return
