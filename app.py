import bottle
import sys, os, string, re
from bottle import route, template, static_file, get, post, request, redirect
from nap import nap
from nap.gamefile import GamefileException

__cwd__ = os.path.dirname(os.path.realpath(__file__))
gamefile_tree = os.environ['GAMEFILE_TREE']

@get('/')
def index():
  return template('home',home=True)

@get('/clubgames')
def clubs():
  wnap = nap.Nap()
  wnap.load_games(gamefile_tree)
  output = wnap.club_games()
  return template('report',title='Qualifier games reported',report=output)

@get('/summary')
def summary():
  wnap = nap.Nap()
  wnap.load_games(gamefile_tree)
  wnap.load_players()
  output = wnap.summary_report()
  return template('report',title='Summary of all qualifiers',report=output)

@get('/flta')
def flta():
  wnap = nap.Nap()
  wnap.load_games(gamefile_tree)
  wnap.load_players()
  output = wnap.flight_report('a',True)
  return template('report',title='Flight A Qualifiers',report=output)

@get('/fltb')
def fltb():
  wnap = nap.Nap()
  wnap.load_games(gamefile_tree)
  wnap.load_players()
  output = wnap.flight_report('b',True)
  return template('report',title='Flight B Qualifiers',report=output)

@get('/fltc')
def fltc():
  wnap = nap.Nap()
  wnap.load_games(gamefile_tree)
  wnap.load_players()
  output = wnap.flight_report('c',True)
  return template('report',title='Flight C Qualifiers',report=output)

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

  upload_nap = nap.Nap()
  is_error = False
  try:
    upload_nap.load_game(gamefile_path)
    upload_nap.load_players()
  except GamefileException, e:
    is_error = True
    error_msg = e.value

  fields = {}
  fields['clubname'] = request.forms.get('clubname')
  fields['testfield'] = request.forms.get('testfield')
  fields['gamefile_name'] = gamefile_filename
  fields['club_dir'] = club_dir
  fields['error_msg'] = error_msg
  fields['is_error'] = is_error

  if is_error:
    fields['club_info'] = ''
    fields['player_summary'] = ''
  else:
    fields['club_info'] = upload_nap.club_games()
    fields['player_summary'] = upload_nap.summary_report()

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

  global wnap
  wnap = nap.Nap()
  wnap.load_games(gamefile_tree)
  wnap.load_players()

  return template('success')

if __name__ == '__main__':
  bottle.run(host='0.0.0.0', port=8080, reloader=True)
else:
  app = application = bottle.default_app()

