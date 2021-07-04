import webapp2
from webapp2_extras.users import users
from webapp2_extras import jinja2
import models.user as user_model
import models.book as book_model


class BooksHandler(webapp2.RequestHandler):
    def get(self):

        usr = users.get_current_user()
        user = user_model.retrieve(usr)

        if usr and user:
            url_usr = users.create_logout_url("/")
            book_list = False
            books = book_model.all_books()
            listBooks = True
            template_values = {
                "books": books,
                "usr": usr,
                "user": user,
                "book_list": book_list,
                "listBooks": listBooks,
                "url_usr": url_usr
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("list_book.html", **template_values))
        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/books', BooksHandler)
], debug=True)
