import time
import bloghandler
import models

class NewComment(bloghandler.BlogHandler):
    def get(self, post_id):
        post = models.Blog.get_by_id(int(post_id), parent=models.blog_key())
        # check if post exists
        if not post:
            return self.error(404)

        # checks if the user is logged in
        if not self.user:
            return self.redirect('/blog/login')

        self.render("newcomment.html")

    def post(self, post_id):
        post = models.Blog.get_by_id(int(post_id), parent=models.blog_key())
        # check if post exists
        if not post:
            return self.error(404)

        # checks if the user is logged in
        if not self.user:
            return self.redirect('/blog/login')

        comment = self.request.get('comment')

        if not comment:
            error = 'Please enter text for your comment'
            return self.render("newcomment.html", comment=comment, error=error)
        # checks if post has any comments
        comment_obj = models.Comment.all().filter('post =', post.key()).get()

        # append comment and update info. if post has comments
        if comment_obj:
            if len(comment_obj.comment_id) == 0:
                cid = 12345
            else:
                cid = int(max(comment_obj.comment_id)) + 1
            comment_obj.comment_count += 1
            comment_obj.commenter.append(self.user.name)
            comment_obj.comment_text.append(comment)
            comment_obj.comment_id.append(str(cid))
            comment_obj.put()
            # add time lag so that user sees updated results
            time.sleep(0.1)
            return self.redirect('/blog/%s' % str(post_id))
        # create comment object if post has no comments
        else:
            cid = 12345
            new_comment_obj = models.Comment(comment_count=1, post=post.key())
            new_comment_obj.commenter.append(self.user.name)
            new_comment_obj.comment_text.append(comment)
            new_comment_obj.comment_id.append(str(cid))
            new_comment_obj.put()
            # add time lag so that user sees updated results
            time.sleep(0.1)
            return self.redirect('/blog/%s' % str(post_id))
