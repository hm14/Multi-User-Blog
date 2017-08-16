import bloghandler
from models import User

# handler for user login for returning signed up users
class Login(bloghandler.BlogHandler):
    def get(self):
        # renders login form
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        # checks if user-provided credentials match relevant entry in database
        u = User.login(username.upper(), password)
        if u:
            # sets secure cookie for successful login
            self.login(u)
            return self.redirect('/blog')
        # prompts user if login fails
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)
