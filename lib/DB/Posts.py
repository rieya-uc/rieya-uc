from google.appengine.ext import db
from google.appengine.api import memcache

class PostsDB(db.Model):
    url = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    tags = db.StringListProperty()
  
    #edited = db.DateTimeProperty()

ACCS = 0
key = "front"
def get_posts():
    posts = memcache.get(key)
    if not posts:
        global ACCS
        ACCS += 1
        posts = db.GqlQuery("SELECT * FROM PostsDB ORDER BY date DESC")
        memcache.set(key, posts)
    return posts

def get_post(url):
    p = memcache.get(url)
    if not p:
        global ACCS
        ACCS += 1
        p = db.GqlQuery("SELECT * FROM PostsDB WHERE url = :1", url)
        if p.get(): memcache.set(url, p)
        else: p = None
    return p
    
def add_post(url, title, content, tags):
    p = PostsDB(url=url, title=title, content=content, tags=tags)
    p.put()

    # update cache
    global ACCS
    ACCS += 1
    memcache.set(url, db.GqlQuery("SELECT * FROM PostsDB WHERE url = :1", url))
    memcache.set(key, db.GqlQuery("SELECT * FROM PostsDB ORDER BY date DESC"))

def accessed():
    return ACCS

