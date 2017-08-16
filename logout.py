import bloghandler

# handler for logging user out of blog by resetting cookie
class Logout(bloghandler.BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog')
