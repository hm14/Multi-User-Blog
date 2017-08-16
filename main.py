import os
import time
import webapp2
import jinja2
import models
import utils
import bloghandler
import postpage
import blogfront
import newpost
import editpost
import newcomment
import editcomment
import likehandler
import unlikehandler
import register
import login
import logout

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


app = webapp2.WSGIApplication([('/blog/?', blogfront.BlogFront),
                               ('/blog/([0-9]+)', postpage.PostPage),
                               ('/blog/newpost', newpost.NewPost),
                               ('/blog/signup', register.Register),
                               ('/blog/login', login.Login),
                               ('/blog/logout', logout.Logout),
                               ('/blog/edit/([0-9]+)', editpost.EditPost),
                               ('/blog/newcomment/([0-9]+)', newcomment.NewComment),
                               ('/blog/editcomment/([0-9]+)', editcomment.EditComment),
                               ('/blog/like/([0-9]+)', likehandler.LikeHandler),
                               ('/blog/unlike/([0-9]+)', unlikehandler.UnlikeHandler)
                              ],
                              debug=True)
