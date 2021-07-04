import webapp2
from webapp2_extras.users import users
from webapp2_extras import jinja2
import models.user as user_model


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()
        user = user_model.retrieve(usr)

        if usr and user:
            return self.redirect("/books")
        else:

            user = user_model.create_empty_user()
            user.nick = "Login"

            url_usr = users.create_login_url("/books")

            template_values = {
                "usr": usr,
                "url_usr": url_usr
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("welcome.html", **template_values))


app = webapp2.WSGIApplication([
    ('/', WelcomeHandler)
], debug=True)
