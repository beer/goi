import cgi
import os
from datetime import datetime
from time import time

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import goi

_DEBUG = True

class MainPage(webapp.RequestHandler):
    def get(self):
	""" init data
	"""

	user = users.get_current_user()
	players = goi.User.all()
	jobs = goi.Job.all()
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
		'jobs': jobs,
		'Msg': msg
		}

	path = os.path.join(os.path.dirname(__file__), 'index.html')
	self.response.out.write(template.render(path, template_values))

class Join(webapp.RequestHandler):
    def post(self):
	player = goi.User()
	if users.get_current_user():
	    player.user = users.get_current_user()
	    player.name = self.request.get('name')
	    player.vigor = 100
	    player.money = 500
	    player.fame = 0
	    player.power = 0
	    player.put()

	self.redirect('/')

class Work(webapp.RequestHandler):
    def post(self):
	job = self.request.get('job')
	player = self.request.get('player')
	hour = self.request.get('hour')
	if hour < 0:
	    hour = 1

	if job and player:
	    job = db.get(job)
	    player = db.get(player)
	    now = int(time())
	    perhour = 60
	    endtime = datetime.fromtimestamp(int(hour) * perhour + now)
	    starttime = datetime.fromtimestamp(now)
	    
	    task = goi.Task(player=player, job=job, category=db.Category('job'),st=starttime, et=endtime)
	    task.put()
	    player.money = player.money + job.salary * int(hour)
	    player.put()


application = webapp.WSGIApplication(
					[('/', MainPage),
					 ('/work', Work),
					 ('/join', Join)],
					debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

