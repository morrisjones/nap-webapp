import bottle
import os
import re
import json
import hashlib
from napemail import confirm_email, send_congrats_email
from bottle import template, request, redirect
from nap.nap import Nap
from nap.gamefile import Player
import logging

reg_app = bottle.Bottle()

valid_pnum = re.compile('^[0-9J-R]\d\d\d\d\d\d')
reg_form_keys = ('game', 'flight', 'player_a', 'pnum_a', 'player_b', 'pnum_b',
         'req_ns', 'email', 'human', 'confirm',)
game_desc = {
  'UF1': "Sunday, October 15, 10:00 a.m., South Bay Bridge Club",
  'UF2': "Sunday, November 5, 10:00 a.m., Long Beach Bridge Club",
}
flight_desc = {
  'a': "A (Open)",
  'b': "B (0-2500)",
  'c': "C (Non-Life Master 0-500)",
}

def qual_players(nap):
  """Build a sorted list of players who appear to have valid ACBL numbers"""
  all_players = sorted(nap.players)
  player_dict = {}
  for p in all_players:
    if bool(valid_pnum.match(p.pnum)):
      player_dict[p.pnum] = "%s, %s" % (p.lname, p.fname)
  return player_dict

@reg_app.get('/')
def home():
  logging.debug("serving /registration")
  return template('reg/home')

@reg_app.get('/show')
def regshow():
  logging.debug("begin /registration/show")
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  reg = {}
  for uf in ('UF1','UF2'):
    reg[uf] = {}
    for flight in ('a','b','c'):
      reg[uf][flight] = {
        'max_table': nap.prereg[uf][flight].find_max_table(),
        'section': nap.prereg[uf][flight].get_section(),
      }
  logging.debug("end /registration/show")
  return template('reg/show',reg=reg)

@reg_app.get('/register')
def regform():
  logging.debug("begin get /registration/register")
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  all_players = sorted(nap.players)
  player_dict = {}
  for p in all_players:
    player_dict[p.pnum] = "%s, %s" % (p.lname, p.fname)

  fields = {
    'players': qual_players(nap),
    'game': 'UF1',
    'flight': 'a',
    'player_a': '',
    'pnum_a': '',
    'player_b': '',
    'pnum_b': '',
    'req_ns': False,
    'email': '',
    'human': '',
  }

  logging.debug("end /registration/register")
  return template('reg/form',fields)

@reg_app.post('/register')
def regsubmit():
  logging.info("begin post /registration/register")
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()

  fields = {}

  for k in reg_form_keys:
    fields[k] = request.forms.get(k)

  error_messages = []

  if not bool(re.match('bridge',fields['human'],re.IGNORECASE)):
    error_messages.append("Please type \"bridge\" in the \"Are you a robot?\" box.")

  if not fields['player_a']:
    error_messages.append("Missing player 1")
  elif not bool(valid_pnum.match(fields['pnum_a'])):
    error_messages.append("Player '%s' isn't found among qualifiers, spelled differently perhaps?" % fields['player_a'])
  else:
    player_a = nap.find_player(fields['pnum_a'])
    if player_a is None:
      error_messages.append("Player not found: %s" % fields['player_a'])
    elif nap.is_already_in_flight(fields['pnum_a'],fields['flight']):
      error_messages.append("Player already registered in flight %s: %s" %
                            (flight_desc[fields['flight']],fields['player_a']))
    elif nap.is_already_in_game(fields['pnum_a'],fields['game']):
      error_messages.append("Player already registered in this game: %s" % (fields['player_a']))

  if not fields['player_b']:
    error_messages.append("Missing player 2")
  elif not bool(valid_pnum.match(fields['pnum_b'])):
    error_messages.append("Player '%s' isn't found among qualifiers, spelled differently perhaps?" % fields['player_b'])
  elif fields['pnum_a'] == fields['pnum_b']:
    error_messages.append("Need two different players (not the same)")
  else:
    player_b = nap.find_player(fields['pnum_b'])
    if player_b is None:
      error_messages.append("Player not found: %s" % fields['player_b'])
    elif nap.is_already_in_flight(fields['pnum_b'],fields['flight']):
      error_messages.append("Player already registered in flight %s: %s" %
                            (flight_desc[fields['flight']],fields['player_b']))
    elif nap.is_already_in_game(fields['pnum_a'],fields['game']):
      error_messages.append("Player already registered in this game: %s" % (fields['player_a']))

  if not fields['email']:
    error_messages.append("Confirmation email address is required")

  if error_messages:
    fields['error_messages'] = error_messages
    fields['players'] = qual_players(nap)
    logging.warning("post /registration/register error messages %s",error_messages)
    return template('reg/form',fields)

  logging.debug("end post /registration/register")
  return template('reg/confirm',fields)

@reg_app.post('/confirm')
def reg_confirm():
  logging.info("start post /registration/confirm")
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()

  fields = {}
  for k in reg_form_keys:
    fields[k] = request.forms.get(k)

  if fields['confirm'] == "no":
    fields['players'] = qual_players(nap)
    return redirect('/registration/')

  reg_form_json = json.dumps(fields, sort_keys=True, indent=4, separators=(',',': '))
  md5 = hashlib.md5()
  md5.update(reg_form_json)
  confirm_key = md5.hexdigest()
  confirm_file = os.path.join(os.environ['UNIT_REGISTRATION'],confirm_key)
  with open(confirm_file,'w') as f:
    f.write(reg_form_json)

  fields['game_desc'] = game_desc[fields['game']]
  fields['flight_desc'] = flight_desc[fields['flight']]

  fields['scheme'], fields['host'] = list(request.urlparts)[:2]

  confirm_email(confirm_key,fields)
  logging.info("New reservation sent for email confirmation: %s" % fields)
  logging.debug("end post /registration/confirm")
  return template('reg/email_sent')

@reg_app.get('/confirm')
def reg_confirm_email():
  logging.debug("begin /confirm")
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()

  confirm_key = request.query.get('key')
  confirm_file = os.path.join(os.environ['UNIT_REGISTRATION'],confirm_key)

  error_messages = []

  if not os.path.isfile(confirm_file):
    error_messages.append("Something went wrong, reservation not found")
    return template('reg/email_confirm',error_messages=error_messages)

  with open(confirm_file,"r") as f:
    reg = json.load(f)
  logging.info("Registration confirmed: %s" % reg)
  if reg['req_ns'] == "on":
    reg['req_ns'] = True
  else:
    reg['req_ns'] = False

  # Check that players are still not already registered
  if reg.get('confirmed') == 'success':
    error_messages.append("This registration has already been confirmed, thank you!")
  else:
    if nap.is_already_in_flight(reg['pnum_a'],reg['flight']):
      error_messages.append("Player %s is already registered in flight %s" % \
                            (reg['player_a'],flight_desc[reg['flight']]))
    if nap.is_already_in_game(reg['pnum_a'],reg['game']):
      error_messages.append("Player %s is already in game %s" % (reg['pnum_a'],reg['game']))
    if nap.is_already_in_flight(reg['pnum_b'],reg['flight']):
      error_messages.append("Player %s is already registered in flight %s" % \
                            (reg['player_b'],flight_desc[reg['flight']]))
    if nap.is_already_in_game(reg['pnum_a'],reg['game']):
      error_messages.append("Player %s is already in game %s" % (reg['pnum_a'],reg['game']))

  if error_messages:
    logging.info("Errors: %s" % error_messages)
    return template('reg/email_confirm',error_messages=error_messages)

  player_a = nap.find_player(reg['pnum_a'])
  if not player_a:
    error_messages.append("Player %s not found in the qualifiers" % reg['player_a'])
  player_b = nap.find_player(reg['pnum_b'])
  if not player_b:
    error_messages.append("Player %s not found in the qualifiers" % reg['player_b'])

  if not error_messages:
    pr = nap.prereg[reg['game']][reg['flight']]
    seat = pr.add_entry(player_a,player_b,reg['req_ns'])
    nap.save_prereg(reg['game'],reg['flight'])
    reg['confirmed'] = "success"
    reg['table_number'] = seat.table
    reg['direction'] = seat.direction
    reg['game_desc'] = game_desc[reg['game']]
    reg['flight_desc'] = flight_desc[reg['flight']]
    logging.info("Registration: %s", reg)
    with open(confirm_file,"w") as f:
      json.dump(reg, f, sort_keys=True, indent=4, separators=(',',': '))

  reg['error_messages'] = error_messages

  send_congrats_email(reg)

  logging.debug("end /confirm")
  return template('reg/email_confirm',**reg)
