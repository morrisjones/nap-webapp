import bottle
import sys, os, string, re
from bottle import route, template, static_file, get, post, request
from nap import nap

__cwd__ = os.path.dirname(os.path.realpath(__file__))
gamefile_tree = os.environ['GAMEFILE_TREE']

# This is a cache of the existing gamefiles
wnap = nap.Nap()
wnap.load_games(gamefile_tree)
wnap.load_players()

@get('/')
def index():
  return template('home')

@get('/clubgames')
def clubs():
  output = wnap.club_games()
  return template('report',title='Qualifier games reported',report=output)

@get('/summary')
def summary():
  output = wnap.summary_report()
  return template('report',title='Summary of all qualifiers',report=output)

@get('/flta')
def flta():
  output = wnap.flight_report('a',True)
  return template('report',title='Flight A Qualifiers',report=output)

@get('/fltb')
def fltb():
  output = wnap.flight_report('b',True)
  return template('report',title='Flight B Qualifiers',report=output)

@get('/fltc')
def fltc():
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
  clubname = request.forms.get('clubname')
  dirname = clubname.translate(None, string.punctuation)
  dirname = dirname.replace(' ','-')
  dirname = dirname.lower()
  gf1_upload = request.files.get('gamefile1')
  gf1_filename = gf1_upload.filename
  save_path = os.path.join(os.environ['GAMEFILE_UPLOADS'],dirname,gf1_filename)
  fields = {}
  fields['clubname'] = request.forms.get('clubname')
  fields['testfield'] = request.forms.get('testfield')
  fields['save_path'] = save_path
  return template('submit_gamefile_confirm',fields)
  
if __name__ == '__main__':
  bottle.run(host='0.0.0.0', port=8080)
else:
  app = application = bottle.default_app()

