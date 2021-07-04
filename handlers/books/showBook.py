import webapp2

from webapp2_extras import jinja2
from webapp2_extras.users import users
import models.user as user_model
import models.book as book_model
import models.comment as comment_model
import models.mybook as mybooks_model


class ShowBookHandler(webapp2.RequestHandler):
    def get(self, key_book):

        usr = users.get_current_user()
        user = user_model.retrieve(usr)
        if usr and user:
            url_usr = users.create_logout_url("/")

            book = book_model.get_book_key(key_book)
            comments = comment_model.get_comment_book(key_book)
            mybooks = mybooks_model.get_mybook_user(key_book, user.email)

            template_values = {
                "book": book,
                "comments": comments,
                "mybooks": mybooks,
                "usr": usr,
                "user": user,
                "url_usr": url_usr
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("show_book.html", **template_values))
        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    (r'/showBook/(.+)', ShowBookHandler)
], debug=True)
