import time

import webapp2
from webapp2_extras import jinja2
from webapp2_extras.users import users

import models.book as book_model
import models.mybook as mybook_model
import models.user as user_model


class AddBookHandler(webapp2.RequestHandler):
    def get(self):

        usr = users.get_current_user()
        user = user_model.retrieve(usr)

        if usr and user:
            url_usr = users.create_logout_url("/")

            template_values = {
                "usr": usr,
                "url_usr": url_usr
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("add_book.html", **template_values))
        else:
            return self.redirect("/")

    def post(self):
        usr = users.get_current_user()
        user = user_model.retrieve(usr)

        if usr and user:
            isbn = self.request.get("isbn")
            exit_book = book_model.get_book(isbn)

            if exit_book is None:

                book = book_model.create_empty_book()
                book.isbn = self.request.get("isbn").strip()
                book.title = self.request.get("title").strip()
                book.author = self.request.get("author").strip()
                book.description = self.request.get("description").strip()
                year = self.request.get("year").strip()
                book.publisher = self.request.get("publisher").strip()

                try:
                    book.year = int(year)
                except ValueError:
                    book.year = 0

                final_book = book_model.create(book)
                final_book.image = self.request.get("image")

                final_book = book_model.update(final_book)
                time.sleep(2)
                self.response.write(final_book.get().key.urlsafe())

                mybook = mybook_model.create_empty_book()
                mybook.book = final_book.get().key.urlsafe()
                mybook.user = user.email
                final_mybook = mybook_model.create(mybook)
                mybook_model.update(final_mybook)
                time.sleep(2)

                return self.redirect("/books")
            else:
                message = "Already exists a book with that isbn! Try with another one or search it"
                self.redirect("/error?message=" + message)

        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/addBook', AddBookHandler)
], debug=True)
