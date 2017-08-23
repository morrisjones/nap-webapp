import bottle

from bottle import route, template

@route('/')
def index():
  return template('<h1>{{message}}</h1>', message="North American Pairs")

if __name__ == '__main__':
  bottle.run(host='0.0.0.0', port=8080)
else:
  app = application = bottle.default_app()

