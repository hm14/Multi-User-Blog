import utils
import bloghandler

# handler for user sign up
class Signup(bloghandler.BlogHandler):
    def get(self):
        # renders sign up form
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        # creates a dictionary for username and email
        params = dict(username=self.username,
                      email=self.email)

        # checks user entered information and prompts user with relevant error
        if not utils.valid_username(self.username):
            params['error_username'] = "Please enter a valid username."
            have_error = True

        if not utils.valid_password(self.password):
            params['error_password'] = "Please enter a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Please make sure your passwords match."
            have_error = True

        if not utils.valid_email(self.email):
            params['error_email'] = "Provide a valid email or leave blank."
            have_error = True

        # renders sign up form again if sign up fails
        if have_error:
            self.render('signup-form.html', **params)
        # registers user in database for successful sign up
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError
