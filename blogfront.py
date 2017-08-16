import bloghandler
from models import Blog

# handler for blog home page i.e. /blog
class BlogFront(bloghandler.BlogHandler):
    def get(self):
        posts = greetings = Blog.all().order('-created')
        self.render('front.html', posts=posts)
