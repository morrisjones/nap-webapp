import bottle
import os, string, re
from bottle import template, static_file, get, post, request, redirect
from nap.nap import Nap
from nap.gamefile import GamefileException, GFUtils
from operator import itemgetter

__cwd__ = os.path.dirname(os.path.realpath(__file__))

#
# This static file block will usually be preempted by NGINX before
# reaching here, but when using the development server it's necessary
#

@get('<:re:.*/><filename:re:.*\.js>')
def javascript(filename):
  print "serving %s" % filename
  return static_file(filename, root="static/js")

@get('<:re:.*/><filename:re:.*\.(ico|png|jpg|gif)>')
def icon(filename):
  print "serving %s" % filename
  return static_file(filename, root="static/img")

@get('<:re:.*/><filename:re:.*\.css>')
def css(filename):
  print "serving %s" % filename
  return static_file(filename, root="static/css")

# --- End of static file service ---

@get('/')
def index():
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
  return template('home',home=True,clubs=club_list,games=games)


@get('/clubgames')
def clubs():
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
  return template('clubgames', fields)


@get('/summary')
def summary():
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
  return template('psummary',
      title='Summary of all qualifiers',
      players=players,
      total_players=total_players,
      flight_totals=flight_totals)


@get('/flta')
def flta():
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  flight_players = nap.flight_players('a')
  return template('flight_players',
                  title='Flight A Qualifiers',
                  flight_players=flight_players)


@get('/fltb')
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


@get('/findplayer')
def findplayer():
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  pnum = request.query['pnum']
  player = nap.find_player(pnum)
  if player:
    qualdates = nap.qualdates[player]
    fields = {
      'name': player.terse(),
      'pnum': player.pnum,
      'flta': ('A' if player.is_qual('a') else ''),
      'fltb': ('B' if player.is_qual('b') else ''),
      'fltc': ('C' if player.is_qual('c') else ''),
      'qualdates': sorted(qualdates),
      'error_msg': None,
    }
  else:
    fields = {
      'pnum': pnum,
      'error_msg': "Player not found"
    }
    
  return template('findplayer',fields)


@get('/findclub')
def findclub():
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  club_num = request.query['club_num']
  if club_num == '999':
    redirect('/')
  club_games = []
  if club_num:
    club_games = nap.club_games(club_number=club_num)
  total_tables = 0.0
  my_player_set = set()
  for game in club_games:
    total_tables += game['tables']
    my_player_set.update(nap.players_from_game(game['game']))
  flight_totals = nap.flight_totals(my_player_set)
  players = []
  for p in sorted(my_player_set):
    players.append({
      'name': p.terse(),
      'pnum': p.pnum,
      'flta': ('Q' if p.is_qual('a') else ''),
      'fltb': ('Q' if p.is_qual('b') else ''),
      'fltc': ('Q' if p.is_qual('c') else ''),
    })
  fields = {
    'title': "Report for club %s" % club_games[0]['club_name'],
    'club_games': club_games,
    'total_games': len(club_games),
    'total_tables': total_tables,
    'flight_totals': flight_totals,
    'players': players,
    'total_players': len(players),
  }
  return template('clubgames',fields)


@get('/findgame')
def findgame():
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  game_index = request.query['game_index']
  if game_index == '999':
    redirect('/')
  club_games = []
  if game_index:
    club_games = nap.club_games(game_index=int(game_index))
  total_tables = 0.0
  my_player_set = set()
  for game in club_games:
    total_tables += game['tables']
    my_player_set.update(nap.players_from_game(game['game']))
  flight_totals = nap.flight_totals(my_player_set)
  players = []
  for p in sorted(my_player_set):
    players.append({
      'name': p.terse(),
      'pnum': p.pnum,
      'flta': ('Q' if p.is_qual('a') else ''),
      'fltb': ('Q' if p.is_qual('b') else ''),
      'fltc': ('Q' if p.is_qual('c') else ''),
    })
  fields = {
    'title': "Report for game %s" % str(int(game_index)+1),
    'club_games': club_games,
    'total_games': len(club_games),
    'total_tables': total_tables,
    'flight_totals': flight_totals,
    'players': players,
    'total_players': len(players),
  }
  return template('clubgames',fields)


#
# Here code for pre-registering for the Unit Final games
#

@get('/regform')
def regform():
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()
  all_players = sorted(nap.players)
  player_dict = {}
  for p in all_players:
    player_dict[p.pnum] = "%s, %s" % (p.lname, p.fname)
  return template('regform',players=player_dict)

@post('/submit_regform')
def submit_regform():
  nap = Nap()
  nap.load_games(os.environ['GAMEFILE_TREE'])
  nap.load_players()

  fields = {}

  fields['game'] = request.forms.get('game')
  fields['flight'] = request.forms.get('flight')
  fields['player_a'] = request.forms.get('player_a')
  fields['player_b'] = request.forms.get('player_b')
  fields['req_ns'] = request.forms.get('req_ns')

  error_messages = []

  getpnum = re.compile('^([^ ]*) \|.*$')
  match = getpnum.match(fields['player_a'])
  a_pnum = match.group(1)
  match = getpnum.match(fields['player_b'])
  b_pnum = match.group(1)

  player_a = nap.find_player(a_pnum)
  if player_a is None:
    error_messages.append("Player not found: %s" % fields['player_a'])
  elif nap.is_already_registered(a_pnum):
    error_messages.append("Player already registered: %s" % fields['player_a'])

  player_b = nap.find_player(b_pnum)
  if player_b is None:
    error_messages.append("Player not found: %s" % fields['player_b'])
  elif nap.is_already_registered(b_pnum):
    error_messages.append("Player already registered: %s" % fields['player_b'])

  pr = nap.prereg[fields['game']][fields['flight']]
  pr.add_entry(player_a,player_b,bool(fields['req_ns']))
  nap.save_prereg(fields['game'],fields['flight'])

  if error_messages:
    # TODO DRY up the repetition here with regform()
    player_dict = {}
    all_players = sorted(nap.players)
    for p in all_players:
      player_dict[p.pnum] = "%s, %s" % (p.lname, p.fname)
    fields['error_messages'] = error_messages
    fields['players'] = player_dict
    return template('regform',fields)

  # Here on the successful processing, send the current registrations to the template
  reg = {}
  for uf in ('UF1','UF2'):
    reg[uf] = {}
    for flight in ('a','b','c'):
      reg[uf][flight] = {
        'max_table': nap.prereg[uf][flight].find_max_table(),
        'section': nap.prereg[uf][flight].get_section(),
      }

  return template('submit_regform',reg=reg)

@get('/confirm_regform')
def confirm_regform():
  return template('confirm_regform')

# end of the webapp

if __name__ == '__main__':
  bottle.run(host='0.0.0.0', port=8080, reloader=True)
else:
  app = application = bottle.default_app()


