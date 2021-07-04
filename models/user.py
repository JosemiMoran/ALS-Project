from google.appengine.api import users
from google.appengine.ext import ndb

from models.enum import Enum


class User(ndb.Model):
    Level = Enum([
        "Admin",
        "Client"
    ], start=400, default=1)
    added = ndb.DateProperty(auto_now_add=True, indexed=True)
    email = ndb.TextProperty(indexed=True)
    nick = ndb.TextProperty(indexed=True)
    level = ndb.IntegerProperty()

    def is_admin(self):
        return self.level == User.Level.Admin or users.is_current_user_admin()

    def is_client(self):
        return self.level == User.Level.Client

    def __str__(self):
        return User.Level.values[self.level] + " (" + self.email + ")"

    def __unicode__(self):
        return User.Level.values[self.level] + ": " + self.nick + " (" + self.email + ")"


def create(usr, level):
    toret = User()

    toret.email = usr.email()
    toret.nick = usr.nickname()
    toret.level = level

    return toret


def create_empty_user():
    return User(email="", nick="", level=User.Level.Client)


@ndb.transactional
def update(user):
    return user.put()


def retrieve(usr):
    toret = None

    if usr:
        usr_email = usr.email()
        found_users = User.query(User.email == usr_email).order(-User.added)

        if (found_users.count() == 0
                and users.is_current_user_admin()):
            toret = create(usr, User.Level.Admin)
            update(toret)
        else:
            if found_users.count() == 0:
                toret = create(usr, User.Level.Client)
                update(toret)
            else:
                toret = found_users.iter().next()
                toret.user_model = usr

    return toret
