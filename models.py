import os
import webapp2
import jinja2
import utils

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# User Model


def users_key(group='default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = utils.make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and utils.valid_pw(name, pw, u.pw_hash):
            return u


# Blog Model


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class Blog(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    author = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    postPermalink = db.StringProperty()

    # used for rendering individual posts (on permalink pages)
    def render(self, user, comments, like_count, error):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html",
                          p=self,
                          user=user,
                          comments=comments,
                          like_count=like_count,
                          error=error)

    # used for rendering all blog posts on blog home page
    def render_p(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("posts.html", p=self)


# Comment Model
class Comment(db.Model):
    post = db.ReferenceProperty(Blog, required=True)
    commenter = db.ListProperty(str, required=True)
    comment_text = db.ListProperty(str, required=True)
    comment_count = db.IntegerProperty(required=True)
    comment_id = db.ListProperty(str)


# Like Model
class Like(db.Model):
    like_count = db.IntegerProperty(default=0)
    post = db.ReferenceProperty(Blog, required=True)
    liked_by = db.ListProperty(int, required=True)
