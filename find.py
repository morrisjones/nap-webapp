import os
import bottle
import logging
from bottle import template, request, redirect
from nap.nap import Nap

find_app = bottle.Bottle()

@find_app.route('/')
def find_home():
  logging.warning("serving /find/ home, useless template")
  return template('findhome')


@find_app.get('/player')
def findplayer():
  logging.debug("begin /find/player")
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

  logging.info("find result for player %s" % pnum)
  logging.debug("end /find/player")
  return template('find/player', fields)

@find_app.get('/club')
def findclub():
  logging.debug("begin /find/club")
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
  logging.info("find result for club %s" % club_num)
  logging.debug("end /find/clubgame")
  return template('find/clubgame',fields)

@find_app.get('/game')
def findgame():
  logging.debug("begin /find/game")
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
  logging.info("find result for game %s" % game_index)
  logging.debug("end /find/game")
  return template('find/clubgame',fields)


