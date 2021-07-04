import webapp2
from webapp2_extras import jinja2
from webapp2_extras.users import users
import models.user as user_model
import models.book as book_model
import models.mybook as mybook_model


class showBooksListHandler(webapp2.RequestHandler):
     def get(self):

        usr = users.get_current_user()
        user = user_model.retrieve(usr)
        book_list = False

        if usr and user:
            url_usr = users.create_logout_url("/")
            mybooks = mybook_model.get_mybooks(user.email)
            books = book_model.all_books()
            key_mybooks = list()

            if mybooks.count() > 0:
                for mybook in mybooks:
                    key_mybooks.append(mybook.book)

                book_list = True
            template_values = {
                "books": books,
                "key_mybook": key_mybooks,
                "book_list": book_list,
                "usr": usr,
                "user": user,
                "url_usr": url_usr
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("list_book.html", **template_values))
        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/showBookList', showBooksListHandler)
], debug=True)
