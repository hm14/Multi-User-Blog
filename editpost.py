import models
import bloghandler
import postpage
import time

from google.appengine.ext import db

# handler for editing and deleting existing posts
class EditPost(postpage.PostPage):
    def get(self, post_id):
        # ensures that user (in this case post author) is logged in
        if self.user:
            key = db.Key.from_path('Blog', int(post_id), parent=models.blog_key())
            post = db.get(key)

            # check if post exists
            if not post:
                return self.error(404)

            if self.user.name != post.author:
                return self.redirect('/blog/%s' % str(post.key().id()))

            # renders post subject and content in edit-post form
            self.render('edit-post.html',
                        subject=post.subject,
                        content=post.content)
        else:
            return self.redirect('/blog/login')

    def post(self, post_id):
        # ensures that user (in this case post author) is logged in
        if not self.user:
            return self.redirect('/blog/login')

        # retrieves post from database so that correct post is edited
        key = db.Key.from_path('Blog', int(post_id), parent=models.blog_key())
        post = db.get(key)

        # check if post exists
        if not post:
            return self.error(404)

        # checks if logged in user and post author are the same
        if self.user.name != post.author:
            return self.redirect('/blog/%s' % str(post.key().id()))

        cancel = self.request.get('cancel')
        deletion1 = self.request.get('deletion1')
        deletion2 = self.request.get('deletion2')
        subject = self.request.get('subject')
        content = self.request.get('content')

        # checks if user confirmed changes or post deletion
        if cancel:
            return self.redirect('/blog/%s' % str(post.key().id()))
        elif deletion1 and deletion2:
            db.delete(key)
            # add time lag so that user sees updated results
            time.sleep(0.1)
            return self.redirect('/blog')

        # prompts user with an error if deletion is not confirmed
        elif deletion1 or deletion2:
                error = "Please check BOTH checkboxes to delete your post"
                self.render("edit-post.html",
                            subject=subject,
                            content=content,
                            error=error)

        else:
            # checks if user deleted subject or post by accident
            if subject and content:
                # updates post entity to reflect user edits
                post.subject = subject
                post.content = content
                post.put()
                # add time lag so that user sees updated results
                time.sleep(0.1)
                # redirects to post page after successful editing
                return self.redirect('/blog/%s' % str(post.key().id()))

            # prompts user with error if both subject and content are missing
            else:
                error = "Please enter BOTH subject and content!"
                self.render("edit-post.html",
                            subject=subject,
                            content=content,
                            error=error)
