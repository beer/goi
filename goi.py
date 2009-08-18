#!/usr/bin/python2.5
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

