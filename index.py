import cgi
import os
import datetime
import time

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

class Job(db.Model):
    name = db.StringProperty()
    salary = db.IntegerProperty()
    wear = db.IntegerProperty()

class GlobalJob(Job):
    extra = db.IntegerProperty()

class Task(db.Model):
    player = db.ReferenceProperty(reference_class=User, collection_name='tasks')
    job = db.ReferenceProperty(reference_class=Job)
    category = db.CategoryProperty()
    st = db.DateTimeProperty(auto_now_add=True)
    et = db.DateTimeProperty()

class MainPage(webapp.RequestHandler):
    def get(self):
	""" init data
	"""

	user = users.get_current_user()
	players = User.all()
	jobs = Job.all()
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
	    now = int(time.time())
	    perhour = 60
	    endtime = datetime.datetime.fromtimestamp(int(hour) * perhour + now)
	    starttime = datetime.datetime.fromtimestamp(now)
	    
	    task = Task(player=player, job=job, category=db.Category('job'),st=starttime, et=endtime)
	    task.put()
	    time.sleep(int(perhour) * int(hour))
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

