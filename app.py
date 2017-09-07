import os, string
from registration import reg_app
from find import find_app
import bottle
from bottle import Bottle, template, static_file, get, post, request, redirect
from nap.nap import Nap
from nap.gamefile import GamefileException, GFUtils
from operator import itemgetter
import logging

__cwd__ = os.path.dirname(os.path.realpath(__file__))
app = application = Bottle()
logging.basicConfig(filename=os.environ['LOG_FILE'],
                    level=os.environ['LOG_LEVEL'],
                    format='%(asctime)s %(levelname)s %(message)s')
logging.info('nap-webapp started')

#
# This static file block will usually be preempted by NGINX before
# reaching here, but when using the development server it's necessary
#

@app.get('<:re:.*/><filename:re:.*\.js>')
def javascript(filename):
  logging.debug("serving %s" % filename)
  return static_file(filename, root="static/js")

@app.get('<:re:.*/><filename:re:.*\.(ico|png|jpg|gif)>')
def icon(filename):
  logging.debug("serving %s" % filename)
  return static_file(filename, root="static/img")

@app.get('<:re:.*/><filename:re:.*\.css>')
def css(filename):
  logging.debug("serving %s" % filename)
  return static_file(filename, root="static/css")

# --- End of static file service ---

@app.get('/')
def index():
  logging.debug("begin /")
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  clubs = nap.get_clubs()
  club_list = []
  for num in clubs:
    club_list.append({
      'num': num,
      'name': clubs[num],
    })
  club_list = sorted(club_list, key=itemgetter('name'))
  game_list = nap.get_game_list()
  games = []
  for g in game_list:
    games.append({
      'date': g.get_game_date(),
      'session': GFUtils.SESSION_STRING[g.get_club_session_num()],
      'name': g.get_club().name,
    })
  logging.debug("end /")
  return template('home',home=True,clubs=club_list,games=games)


@app.get('/clubgames')
def clubs():
  logging.debug("begin /clubgames")
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  club_games = nap.club_games()
  total_tables = 0.0
  for g in club_games:
    total_tables += g['tables']
  fields = {
    'title': "Qualifier games reported",
    'club_games': club_games,
    'total_games': len(club_games),
    'total_tables': total_tables,
    'flight_totals': None,
    'players': None,
  }
  logging.debug("end /clubgames")
  return template('clubgames', fields)


@app.get('/summary')
def summary():
  logging.debug("begin /summary")
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  total_players = len(nap.players)
  flight_totals = nap.flight_totals()
  players = []
  for p in sorted(nap.players):
    players.append({
      'name': p.terse(),
      'pnum': p.pnum,
      'flta': ('Q' if p.is_qual('a') else ''),
      'fltb': ('Q' if p.is_qual('b') else ''),
      'fltc': ('Q' if p.is_qual('c') else ''),
    })
  logging.debug("end /summary")
  return template('psummary',
      title='Summary of all qualifiers',
      players=players,
      total_players=total_players,
      flight_totals=flight_totals)


@app.get('/flta')
def flta():
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  flight_players = nap.flight_players('a')
  return template('flight_players',
                  title='Flight A Qualifiers',
                  flight_players=flight_players)


@app.get('/fltb')
def fltb():
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  flight_players = nap.flight_players('b')
  return template('flight_players',
                  title='Flight A Qualifiers',
                  flight_players=flight_players)


@get('/fltc')
def fltc():
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  flight_players = nap.flight_players('c')
  return template('flight_players',
                  title='Flight A Qualifiers',
                  flight_players=flight_players)

@app.get('/submit_gamefile')
def submit_gamefile_form():
  logging.debug("end /submit_gamefile")
  return template('submit_gamefile')

@app.post('/submit_gamefile_confirm')
def submit_gamefile_result():
  logging.debug("start post /submit_gamefile_confirm")
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
    nap = Nap()
    nap.load_games(os.environ['GAMEFILE_TREE'])
    all_games = nap.games
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
    fields['club_info'] = upload_nap.club_games_report()
    fields['player_summary'] = upload_nap.summary_report()
  else:
    fields['club_info'] = ''
    fields['player_summary'] = ''

  if is_error:
    logging.warning("Returning error message on gamefile submission %s" % error_msg)
  logging.debug("end /submit_gamefile_confirm")
  return template('submit_gamefile_confirm',fields)


@app.post('/confirm_gamefile')
def confirm_gamefile():
  logging.debug("begin post /confirm_gamefile")
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

  logging.info('New gamefile uploaded club: %s file: %s' % (club_dir,gamefile_name))
  logging.debug("end post /confirm_gamefile")
  return template('success')


@app.get('/appnotes')
def appnotes():
  logging.debug("visit /appnotes")
  return template('appnotes')

@app.get('/find<path:re:.*$>')
def find_redirect(path):
  logging.warning("Old /find URL used and redirected")
  redir = '/find/' + path
  if request.query:
    redir += '?'
    queries = []
    for param in request.query:
      queries.append("%s=%s" % (param,request.query[param]))
    redir += '&'.join(queries)
  return redirect(redir)

@app.get('/find')
def find_():
  return redirect('/find/')

app.mount('/find/',find_app)


#
# Here code for pre-registering for the Unit Final games
#

@app.get('/registration')
def registration():
  return redirect('/registration/')

app.mount('/registration/',reg_app)

@app.get('/regform<path:re:.*$>')
def regform_redirect(path):
  redirect('/registration' + path)

# end of the webapp

if __name__ == '__main__':
  bottle.run(app=app, host='0.0.0.0', port=8080, reloader=True)


