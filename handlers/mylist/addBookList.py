import webapp2
import os
from webapp2_extras import jinja2
from webapp2_extras.users import users
from google.appengine.api import images
import models.user as user_model
import models.book as book_model
import models.mybook as mybook_model
import time


class AddBookListHandler(webapp2.RequestHandler):
    def get(self):

        usr = users.get_current_user()
        user = user_model.retrieve(usr)

        if usr and user:
            url_usr = users.create_logout_url("/")
            idBook = self.request.GET["idBook"]

            mybook = mybook_model.get_mybook_user(idBook, user.email)

            if mybook:
                mybook_model.create_query_delete_one(mybook)
                time.sleep(2)
                return self.redirect("/showBook/" + idBook)
            else:
                mybook = mybook_model.create_empty_book()
                mybook.book = idBook
                mybook.user = user.email
                final_mybook = mybook_model.create(mybook)
                mybook_model.update(final_mybook)
                time.sleep(2)

                return self.redirect("/showBook/" + idBook)
        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/addBookList', AddBookListHandler)
], debug=True)
