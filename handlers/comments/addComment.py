import webapp2

from webapp2_extras import jinja2
from webapp2_extras.users import users
import models.user as user_model
import models.comment as comment
import time


class AddCommentHandler(webapp2.RequestHandler):

    def post(self):
        usr = users.get_current_user()
        user = user_model.retrieve(usr)

        if user_model and user:
            keyBook = self.request.GET["idBook"]
            # self.request.path_url()
            content = self.request.get("commentBook")
            c = comment.create_empty_comment()
            c.content = content
            c.book = keyBook
            c.user = user.email

            final_comment = comment.create(c)
            comment.update(final_comment)
            time.sleep(1)
            return self.redirect("/showBook/" + keyBook)

        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/addComment', AddCommentHandler)
], debug=True)
