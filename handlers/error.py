import webapp2
from webapp2_extras.users import users
from webapp2_extras import jinja2
import models.user as user_model
import models.book as book_model


class ErrorHandler(webapp2.RequestHandler):
    def get(self):

        usr = users.get_current_user()
        user = user_model.retrieve(usr)

        if usr and user:
            url_usr = users.create_logout_url("/")
            message = self.request.GET["message"]
            url = self.request.GET["url"]

            template_values = {
                "message": message,
                "url": url,
                "usr": usr,
                "user": user,
                "url_usr": url_usr
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("error.html", **template_values))
        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/error', ErrorHandler)
], debug=True)
