import bottle

import sys, os
from bottle import route, template
import StringIO
from nap import nap

__cwd__ = os.path.dirname(os.path.realpath(__file__))

@route('/')
def index():
  return template('<h1>{{message}}</h1>', message="North American Pairs")

@route('/clubs')
def clubs():
  output = nap.main(__cwd__,["-c"])
  return output
  

if __name__ == '__main__':
  bottle.run(host='0.0.0.0', port=8080)
else:
  app = application = bottle.default_app()

