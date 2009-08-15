import cgi
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class User(db.Model):
    user = db.UserProperty()
    name = db.StringProperty()
    vigor = db.IntegerProperty()
    money = db.IntegerProperty()
    fame = db.IntegerProperty()
    power = db.IntegerProperty()

class MainPage(webapp.RequestHandler):
    def get(self):
	user = users.get_current_user()
	players = User.all()
	if user:
	    msg = 'Hello! ' + user.nickname()
	    url = users.create_logout_url(self.request.uri)
	    label = 'Logout'
	    player = db.GqlQuery("SELECT * FROM User WHERE user = :1", user).get()
	else:
	    url = users.create_login_url(self.request.uri)
	    msg = 'Hey ! Join us.'
	    label = 'Login'
	    player = ''

	template_values = {
		'Title': 'God of Investment',
		'Url': url,
		'Label': label,
		'player': player,
		'players': players,
		'Msg': msg
		}

	path = os.path.join(os.path.dirname(__file__), 'index.html')
	self.response.out.write(template.render(path, template_values))

class Join(webapp.RequestHandler):
    def post(self):
	player = User()
	if users.get_current_user():
	    player.user = users.get_current_user()
	    player.name = self.request.get('name')
	    player.vigor = 100
	    player.money = 500
	    player.fame = 0
	    player.power = 0
	    player.put()

	self.redirect('/')



application = webapp.WSGIApplication(
					[('/', MainPage),
					 ('/join', Join)],
					debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

