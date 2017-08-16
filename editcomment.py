import time
import bloghandler
import models

class EditComment(bloghandler.BlogHandler):
    def get(self, post_id):
        post = models.Blog.get_by_id(int(post_id), parent=models.blog_key())
        cid = self.request.get('cid')

        # check if post exists
        if not post:
            return self.error(404)

        # checks if the user is logged in
        if not self.user:
            return self.redirect('/blog/login')

        # check if post has any comments
        comment_obj = models.Comment.all().filter('post =', post.key()).get()
        if not comment_obj:
            return self.redirect('/blog/%s' % str(post_id))

        # check if comment to be edited exists for relevant post
        comment_obj = models.Comment.all().filter('post =', post.key()).get()
        if cid not in comment_obj.comment_id:
            return self.redirect('/blog/%s' % str(post_id))

        cid_index = comment_obj.comment_id.index(cid)

        # check if comment to be edited was created by logged in user
        if comment_obj.commenter[cid_index] != self.user.name:
            return self.redirect('/blog')

        self.render("edit-comment.html",
                    comment=comment_obj.comment_text[cid_index])

    def post(self, post_id):
        post = models.Blog.get_by_id(int(post_id), parent=models.blog_key())
        cid = self.request.get('cid')

        # check if post exists
        if not post:
            return self.error(404)

        # checks if the user is logged in
        if not self.user:
            return self.redirect('/blog/login')

        # check if post has any comments
        comment_obj = models.Comment.all().filter('post =', post.key()).get()
        if not comment_obj:
            return self.redirect('/blog/%s' % str(post_id))

        # check if comment to be edited exists for relevant post
        comment_obj = models.Comment.all().filter('post =', post.key()).get()
        if cid not in comment_obj.comment_id:
            return self.redirect('/blog/%s' % str(post_id))

        cid_index = comment_obj.comment_id.index(cid)

        if comment_obj.commenter[cid_index] != self.user.name:
            return self.redirect('/blog')

        comment = self.request.get('comment')
        cancel = self.request.get('cancel')
        deletion1 = self.request.get('deletion1')
        deletion2 = self.request.get('deletion2')

        # checks if user confirmed changes or post deletion
        if cancel:
            return self.redirect('/blog/%s' % str(post_id))
        elif deletion1 and deletion2:
            comment_obj.comment_count -= 1
            del comment_obj.commenter[cid_index]
            del comment_obj.comment_text[cid_index]
            del comment_obj.comment_id[cid_index]
            comment_obj.put()
            # add time lag so that user sees updated results
            time.sleep(0.1)
            return self.redirect('/blog/%s' % str(post_id))

        # prompts user with an error if deletion is not confirmed
        elif deletion1 or deletion2:
                error = "Please check BOTH checkboxes to delete your comment"
                self.render("edit-comment.html",
                            comment=comment_obj.comment_text[cid_index],
                            error=error)

        else:
            # checks if user deleted text of comment by accident
            if comment:
                # updates post entity to reflect user edits
                comment_obj.comment_text[cid_index] = comment
                comment_obj.put()
                time.sleep(0.1)

                # redirects to post page after successful editing
                return self.redirect('/blog/%s' % str(post.key().id()))

            # prompts user with error if both subject and content are missing
            else:
                error = "You cannot post a blank comment."
                self.render("edit-comment.html",
                            comment=comment_obj.comment_text[cid_index],
                            error=error)
