#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
from datetime import datetime
from google.appengine.ext import db
#from lib.DB.Posts import Posts
import lib.DB.Posts as Posts
import string

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
        autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class FrontPageHandler(Handler):
    def render_page(self):
        posts = Posts.get_posts()
        self.render("blogfront.html",posts=posts, message="")

    def get(self):
        self.render_page()

class PermaHandler(Handler):
    def render_page(self,post=""):
        self.render("blogfront.html",posts=post,message="perma")

    def get(self,pid):
        p = Posts.get_post(pid)
        #if p == None:
        #    self.write("None")
        #else:
        #    self.write(p.content)
        self.render_page(p) if p else self.redirect("/404")
    
class NewPostHandler(Handler):
    def render_page(self):
        self.render("newpost.html")

    def get(self):
        self.render_page()

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        tags = self.request.get("tags")


        if title and content:
            url_date = datetime.now().strftime("%Y-%m-%d")
            url_title = str(title).translate(string.maketrans("",""), \
                                             string.punctuation)
            url = url_date + "/" + url_title.lower().replace(" ","-")

            content = content.replace("\n", "<br>")  # preserve paragraphs
            
            t = tags.split() if tags else []
            
            Posts.add_post(url, title, content, t)
            self.redirect("/p/"+url)
        else:
            self.write("error posting")
        return

def ErrorHandler(Handler):
    def get(self):
        self.error(404)
        #self.write("404, page not found")

app = webapp2.WSGIApplication([('/',FrontPageHandler),
                               ('/newpost',NewPostHandler),
                               ('/p/([0-9a-z-//]+)', PermaHandler),
                               ('/*.', ErrorHandler),
                               ],
                               debug=True)



