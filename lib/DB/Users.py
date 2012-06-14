from google.appengine.ext import db

class Users(db.Model):
    user_id = db.StringProperty(required=True)
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
