import bottle
import os
import re
import json
import hashlib
from napemail import confirm_email
from bottle import template, request, redirect
from nap.nap import Nap
import logging

reg_app = bottle.Bottle()

valid_pnum = re.compile('^[0-9J-R]\d\d\d\d\d\d')
reg_form_keys = ('game', 'flight', 'player_a', 'pnum_a', 'player_b', 'pnum_b',
         'req_ns', 'email', 'human', 'confirm',)

def qual_players(nap):
  """Build a sorted list of players who appear to have valid ACBL numbers"""
  all_players = sorted(nap.players)
  player_dict = {}
  for p in all_players:
    if bool(valid_pnum.match(p.pnum)):
      player_dict[p.pnum] = "%s, %s" % (p.lname, p.fname)
  return player_dict

@reg_app.get('/show')
def regshow():
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
  return template('reg/show',reg=reg)

@reg_app.get('/')
def regform():
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

  return template('reg/form',fields)

@reg_app.post('/')
def regsubmit():
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()

  fields = {}

  for k in reg_form_keys:
    fields[k] = request.forms.get(k)

  error_messages = []

  if fields['human'] != 'bridge':
    error_messages.append("Please type \"bridge\" in the \"Are you a robot?\" box.")

  if not fields['player_a']:
    error_messages.append("Missing player 1")
  elif not bool(valid_pnum.match(fields['pnum_a'])):
    error_messages.append("Player 1 appears to have an invalid ACBL number")
  else:
    player_a = nap.find_player(fields['pnum_a'])
    if player_a is None:
      error_messages.append("Player not found: %s" % fields['player_a'])
    elif nap.is_already_registered(fields['pnum_a']):
      error_messages.append("Player already registered: %s" % fields['player_a'])

  if not fields['player_b']:
    error_messages.append("Missing player 2")
  elif not bool(valid_pnum.match(fields['pnum_b'])):
    error_messages.append("Player 2 appears to have an invalid ACBL number")
  else:
    player_b = nap.find_player(fields['pnum_b'])
    if player_b is None:
      error_messages.append("Player not found: %s" % fields['player_b'])
    elif nap.is_already_registered(fields['pnum_b']):
      error_messages.append("Player already registered: %s" % fields['player_b'])

  if not fields['email']:
    error_messages.append("Confirmation email address is required")

  if error_messages:
    fields['error_messages'] = error_messages
    fields['players'] = qual_players(nap)
    return template('reg/form',fields)

  # else:
  #   pr = nap.prereg[fields['game']][fields['flight']]
  #   pr.add_entry(player_a,player_b,bool(fields['req_ns']))
  #   nap.save_prereg(fields['game'],fields['flight'])

  return template('reg/confirm',fields)

@reg_app.post('/confirm')
def reg_confirm():
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

  if fields['game'] == 'UF1':
    fields['long_game'] = "October 15, 10:00 a.m., South Bay Bridge Club"
  elif fields['game'] == 'UF2':
    fields['long_game'] = "November 5, 10:00 a.m., Long Beach Bridge Club"
  if fields['flight'] == 'a':
    fields['long_flight'] = 'A (Open)'
  if fields['flight'] == 'b':
    fields['long_flight'] = 'B (0-2500)'
  if fields['flight'] == 'c':
    fields['long_flight'] = 'C (Non-Life Master 0-500)'

  confirm_email(confirm_key,fields)
  logging.info("New reservation sent for email confirmation: %s" % fields)

  return redirect('show')

@reg_app.get('/confirm')
def reg_confirm_email():
  return template('email_confirm')