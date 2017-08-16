import time
import bloghandler
import models

class UnlikeHandler(bloghandler.BlogHandler):
    def get(self, post_id):
        post = models.Blog.get_by_id(int(post_id), parent=models.blog_key())

        # check if post exists
        if not post:
            return self.error(404)

        #  checks if the user is logged in
        if not self.user:
            return self.redirect('/blog')

        #  checks if the logged in user is also the owner of the post
        if self.user.name.upper() == post.author:
            error = '1'
            return self.redirect('/blog/%s?error=%s' % (str(post_id), error))

        #  checks if the user has already liked the post
        like_obj = models.Like.all().filter('post =', post.key()).get()

        if like_obj:
            # decreases like_count and removes user from list of user_ids
            if self.user.key().id() in like_obj.liked_by:
                like_obj.liked_by.remove(self.user.key().id())
                like_obj.like_count -= 1
                like_obj.put()
                # add time lag so that user sees updated results
                time.sleep(0.1)
                return self.redirect('/blog/%s' % (str(post_id)))

        error = '3'
        return self.redirect('/blog/%s?error=%s' % (str(post_id), error))
