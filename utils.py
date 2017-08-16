import os
import re
import hashlib
import hmac
import random
import jinja2

from string import letters

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# secret for hashing cookies
secret = 'duwdjsd73857384ur34'


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


# checks if username entered by user is an acceptable username
def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)


# checks if username entered by user is an acceptable password
def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return password and PASS_RE.match(password)


# checks if username entered by user is an acceptable email
def valid_email(email):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or EMAIL_RE.match(email)

# creates hashed cookie as: secret|(hash of cookie and secret)
def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())


# checks if a cookie is valid or tampered with
def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


# creates random string of 5 characters for securing passwords
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


# creates password hash using username and password, and salt
def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


# checks user provided password against saved password
def valid_pw(name, password, h):
    # separates salt
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)
