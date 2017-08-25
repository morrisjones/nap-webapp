import bottle
import sys, os, string, re
from bottle import route, template, static_file, get, post, request, redirect
from nap.nap import Nap
from nap.gamefile import GamefileException
from __version__ import __version__

__cwd__ = os.path.dirname(os.path.realpath(__file__))
gamefile_tree = os.environ['GAMEFILE_TREE']

@get('/')
def index():
  return template('home',home=True)

@get('/clubgames')
def clubs():
  gnap = Nap()
  gnap.load_games(gamefile_tree)
  output = gnap.club_games()
  return template('report',title='Qualifier games reported',report=output)

@get('/summary')
def summary():
  gnap = Nap()
  gnap.load_games(gamefile_tree)
  gnap.load_players()
  output = gnap.summary_report()
  return template('report',title='Summary of all qualifiers',report=output)

@get('/flta')
def flta():
  gnap = Nap()
  gnap.load_games(gamefile_tree)
  gnap.load_players()
  flight_players = gnap.flight_players('a')
  return template('flight_players',
                  title='Flight A Qualifiers',
                  flight_players=flight_players)

@get('/fltb')
def fltb():
  gnap = Nap()
  gnap.load_games(gamefile_tree)
  gnap.load_players()
  flight_players = gnap.flight_players('b')
  return template('flight_players',
                  title='Flight A Qualifiers',
                  flight_players=flight_players)

@get('/fltc')
def fltc():
  gnap = Nap()
  gnap.load_games(gamefile_tree)
  gnap.load_players()
  flight_players = gnap.flight_players('c')
  return template('flight_players',
                  title='Flight A Qualifiers',
                  flight_players=flight_players)

@get('/favicon.ico')
def favicon():
  return static_file("favicon.ico", root="./static/img")

@get('/submit_gamefile')
def submit_gamefile_form():
  return template('submit_gamefile')

@post('/submit_gamefile_confirm')
def submit_gamefile_result():

  # First check for robots
  if request.forms.get('testfield') != 'bridge':
    return template('no_robots')

  # Use the clubname to make a subdirectory for the gamefile
  clubname = request.forms.get('clubname')
  club_dir = clubname.translate(None, string.punctuation)
  club_dir = club_dir.replace(' ','-')
  club_dir = club_dir.lower()

  gf1_upload = request.files.get('gamefile1')
  gamefile_filename = gf1_upload.filename

  error_msg = "No errors :)"
  gamefile_dir = os.path.join(os.environ['GAMEFILE_UPLOADS'],club_dir)
  gamefile_path = os.path.join(gamefile_dir,gamefile_filename)
  if not os.path.exists(gamefile_dir):
    os.makedirs(gamefile_dir)
  if os.path.isfile(gamefile_path):
    os.remove(gamefile_path)
    error_msg = "Note: Replacing previous uploaded file"
  gf1_upload.save(gamefile_path)

  is_error = False
  try:
    upload_nap = Nap()
    upload_game = upload_nap.load_game(gamefile_path)
    upload_game_key = upload_game.get_key()
    upload_nap.load_players()
  except GamefileException, e:
    is_error = True
    error_msg = e.value

  # Check to see if this game is already in the data set
  if not is_error:
    gnap = Nap()
    gnap.load_games(gamefile_tree)
    all_games = gnap.games
    if upload_game_key in all_games:
      is_error = True
      error_msg = "This game appears to be in the data set already."

  fields = {}
  fields['clubname'] = request.forms.get('clubname')
  fields['testfield'] = request.forms.get('testfield')
  fields['gamefile_name'] = gamefile_filename
  fields['club_dir'] = club_dir
  fields['error_msg'] = error_msg
  fields['is_error'] = is_error

  if not is_error:
    fields['club_info'] = upload_nap.club_games()
    fields['player_summary'] = upload_nap.summary_report()
  else:
    fields['club_info'] = ''
    fields['player_summary'] = ''

  return template('submit_gamefile_confirm',fields)
  
@post('/confirm_gamefile')
def confirm_gamefile():
  confirm = request.forms.get('confirm')
  gamefile_name = request.forms.get('gamefile_name')
  club_dir = request.forms.get('club_dir')

  if confirm != 'yes':
    redirect('/')
    return

  src_file = os.path.join(os.environ['GAMEFILE_UPLOADS'],club_dir,gamefile_name)
  dest_path = os.path.join(os.environ['GAMEFILE_TREE'],club_dir)
  dest_file = os.path.join(dest_path,gamefile_name)
  if not os.path.exists(dest_path):
    os.makedirs(dest_path)
  if os.path.isfile(dest_file):
    version = 1
    backup = "%s.%s" % (dest_file,version)
    while os.path.isfile(backup):
      version += 1
      backup = "%s.%s" % (dest_file,version)
    os.rename(dest_file,backup)
  os.rename(src_file,dest_file)

  return template('success')

@get('/appnotes')
def appnotes():
  return template('appnotes')

if __name__ == '__main__':
  bottle.run(host='0.0.0.0', port=8080, reloader=True)
else:
  app = application = bottle.default_app()

