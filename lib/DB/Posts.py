from google.appengine.ext import db
from google.appengine.api import memcache

class PostsDB(db.Model):
    url = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    tags = db.StringListProperty()
    edited = db.DateTimeProperty()

key = "front"
def get_posts():
    posts = memcache.get(key)
    if not posts:
        posts = db.GqlQuery("SELECT * FROM PostsDB ORDER BY date DESC")
        memcache.set(key, posts)
    return posts

def get_post(url):
    p = memcache.get(url)
    if not p:
        p = db.GqlQuery("SELECT * FROM PostsDB WHERE url = :1", url)
        if p.get(): memcache.set(url, p.get())
        else: p = None
    return p
    
def add_post(url, title, content, tags=[]):
    p = PostsDB(url=url, title=title, content=content, tags=tags)
    p.put()

    # update cache
    memcache.set(url, db.GqlQuery("SELECT * FROM PostsDB WHERE url = :1", url))
    memcache.set(key, db.GqlQuery("SELECT * FROM PostsDB ORDER BY date DESC"))

def edit_post(url, title, content, tags):
    p = memcache.get(url)
    if p:
        p.title = title
        p.content = content
        p.tags = tags
        db_post = db.GqlQuery("SELECT * FROM PostsDB WHERE url = :1", url).get()
        db_post.title = title
        db_post.content = content
        db_post.tags = tags
        db_post.put()
    else:
        p = PostsDB(url=url, title=title, content=content, tags=tags)
        p.put()
    memcache.set(key, db.GqlQuery("SELECT * FROM PostsDB ORDER BY date DESC"))
    memcache.set(url, p)


