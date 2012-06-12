from google.appengine.ext import db

class Posts(db.Model):
    url = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    tags = db.StringListProperty()
    #edited = db.DateTimeProperty()

# Blog accounts
class Users(db.Model):
    user_id = db.StringProperty(required=True)
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
