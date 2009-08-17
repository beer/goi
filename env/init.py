from google.appengine.ext import db

class Job(db.Model):
    name = db.StringProperty()
    salary = db.IntegerProperty()
    wear = db.IntegerProperty()

jobs = Job.all()
if jobs:
    db.delete(jobs)

j = Job(name="beggar",salary=20,wear=2)
j.put()
j = Job(name="waiter",salary=60,wear=6)
j.put()
