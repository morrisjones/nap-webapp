import bottle

import sys, os
from bottle import route, template
import StringIO
from nap import nap

__cwd__ = os.path.dirname(os.path.realpath(__file__))
gamefile_tree = os.environ['GAMEFILE_TREE']

@route('/')
def index():
  return template('home')

@route('/clubgames')
def clubs():
  output = nap.main(__cwd__,["-t",gamefile_tree,"-c"])
  return template('report',title='Qualifier games reported',report=output)

@route('/summary')
def clubs():
  output = nap.main(__cwd__,["-t",gamefile_tree,"-s"])
  return template('report',title='Summary of all qualifiers',report=output)


if __name__ == '__main__':
  bottle.run(host='0.0.0.0', port=8080)
else:
  app = application = bottle.default_app()

