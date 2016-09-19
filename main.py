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

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Story(db.Model):
    title = db.StringProperty(required=True)
    story = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    """docstring for St"""

    # replace this with some code to handle the request,m


class Handler(webapp2.RequestHandler):
    # def get(self):
    # self.response.write()
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class ViewPostHandler(webapp2.RequestHandler):
    """docstring for ViewPostHandler"""
    def get(self, id):
        story = Story.get_by_id(int(id))
        self.response.write(story.title)


class MainPageHandler(Handler):
    def render_blog(self, title="", story="", error=""):
        storys = db.GqlQuery("SELECT * FROM Story ORDER BY created DESC")

        self.render("blog.html", storys=storys)

    def get(self):
        self.render_blog()

    def post(self):
        title = self.request.get("title")
        story = self.request.get("story")

        if title and story:
            a = Story(title=title, story=story)
            a.put()
            self.redirect("/")

        else:
            error = "we need both a title and a story!"
            self.render_blog(title, story, error)

app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
