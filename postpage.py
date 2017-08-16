import os
import jinja2
import webapp2
import models
import bloghandler

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# handler for displaying individual blog posts
class PostPage(bloghandler.BlogHandler):
    def get(self, post_id):
        # redirects user to blog home page if user is not logged in/signed up
        if not self.user:
            return self.redirect('/blog')

        # retrieves post entity from database so correct post is displayed
        post = models.Blog.get_by_id(int(post_id), parent=models.blog_key())

        error = self.request.get('error')

        # evaluates error based on the error passed from Like/Unlikehandler
        if error == '1':
            error = 'You cannot like or unlike your own post!'
        elif error == '2':
            error = 'You cannot like a post twice!'
        elif error == '3':
            error = 'You cannot unlike a post that you have not liked before.'
        else:
            error = ''

        if not post:
            return self.redirect('/blog/login')

        comment_obj = models.Comment.all().filter('post =', post.key()).get()
        comment_count = 0
        if comment_obj:
            comment_count = comment_obj.comment_count

        like_obj = models.Like.all().filter('post =', post.key()).get()
        like_count = 0
        if like_obj:
            like_count = like_obj.like_count
        # passes post to be displayed to permalink page created for the post
        self.render("permalink.html",
                    post=post,
                    user=self.user,
                    comments=comment_obj,
                    like_count=like_count,
                    error=error)

    def post(self, post_id):
        # redirects user to home page if user is not logged in/signed up
        if not self.user:
            return self.redirect('/blog')

        # retrieves post from the database for display/edits/deletion
        key = db.Key.from_path('Blog', int(post_id), parent=models.blog_key())
        post = db.get(key)

        if not post:
            return self.redirect('/blog/login')

        error = ''
        comment_obj = Comment.all().filter('post =', post.key()).get()
        comment_count = 0
        if comment_obj:
            comment_count = comment_obj.comment_count
            error = 'comment_obj exists'

        like_obj = Like.all().filter('post =', post.key()).get()
        like_count = 0
        if like_obj:
            like_count = like_obj.like_count

        self.render("permalink.html",
                    post=post,
                    user=self.user,
                    comments=comment_obj,
                    like_count=like_count,
                    error=error)
