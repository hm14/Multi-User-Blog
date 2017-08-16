import signup
from models import User

# handles user registeration for new user signing up
class Register(signup.Signup):
    def done(self):
        # checks if username requested by user already exists
        u = User.by_name(self.username.upper())
        # prevents username duplication by showing an error
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username=msg)
        # registers user in database after successfu sign up
        else:
            u = User.register(self.username.upper(),
                              self.password,
                              self.email)
            u.put()

            # sets secure cookie for user upon successful sign up
            self.login(u)

            # redirects user to homepage upon successful signup
            self.redirect('/blog')
