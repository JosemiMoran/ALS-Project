from google.appengine.ext import ndb


class Comment(ndb.Model):
    added = ndb.DateProperty(auto_now_add=True, indexed=True)
    content = ndb.TextProperty(required=True)
    book = ndb.StringProperty(required=True)
    user = ndb.StringProperty(required=True)


def get_comment_book(key_book):
    return Comment.query(Comment.book == key_book).order(Comment.added)


def create(com):
    comment = Comment()
    comment.content = com.content
    comment.book = com.book
    comment.user = com.user

    return comment


def create_empty_comment():
    comment = Comment()
    comment.content = ""
    comment.book = ""
    comment.user = ""

    return comment


@ndb.transactional
def update(comment):
    return comment.put()
