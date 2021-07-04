from google.appengine.ext import ndb
from google.appengine.api import users
from models.enum import Enum


class User(ndb.Model):
    Level = Enum([
        "Admin",  # Can do anything
        "Client"  # Can just read and make comments.
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
    """Creates a new user object, from GAE's user object.
        :param usr: The GAE user object.
        :param level: The desired level.
        :return: A new User object."""
    toret = User()

    toret.email = usr.email()
    toret.nick = usr.nickname()
    toret.level = level

    return toret


def create_empty_user():
    """Used when there the user is not important."""
    return User(email="", nick="", level=User.Level.Client)


@ndb.transactional
def update(user):
    """Updates a user.
        :param user: The user to update.
        :return: The key of the record.
    """
    return user.put()


def retrieve(usr):
    """Reads the user info from the database.
    :param usr: The GAE user object.
    :return: The User retrieved, or a client created appropriately if not found.
    """
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
