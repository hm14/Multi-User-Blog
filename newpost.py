import models
import bloghandler

# handler for creating a new post
class NewPost(bloghandler.BlogHandler):
    def get(self):
        # ensures that only logged in users can create posts
        if self.user:
            self.render("newpost.html")
        else:
            return self.redirect('/blog/login')

    def post(self):
        # ensures that only logged in users can create posts
        if not self.user:
            return self.redirect('/blog/login')

        subject = self.request.get('subject')
        content = self.request.get('content')
        # sets author to currently logged in user
        author = self.user.name.upper()

        # checks if user entered both subject and content for the post
        if subject and content:
            # creates a new entity for the post entered by the user
            p = models.Blog(parent=models.blog_key(),
                     subject=subject,
                     content=content,
                     author=author,
                     postPermalink='')
            # adds created entity in the database
            p.put()
            p.postPermalink = '%s' % str(p.key().id())
            # adds created entity in the database with permalink
            p.put()
            # redirects user to new post's permalink page
            return self.redirect('/blog/%s' % str(p.key().id()))

        else:
            error = "Please enter BOTH subject and content!"
            # preserves user entered subject or content entries in form
            self.render("newpost.html",
                        subject=subject,
                        content=content,
                        error=error)
