from google.appengine.ext import db

class Story(db.Model):
    title = db.StringProperty()
    body = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)

s = Story()
s.title = "The Three Little Pigs"
s.put()
