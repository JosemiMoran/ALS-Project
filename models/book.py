from google.appengine.ext import ndb


class Book(ndb.Model):
    isbn = ndb.StringProperty(indexed=True, required=True)
    title = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=True)
    year = ndb.StringProperty(required=True)
    image = ndb.BlobProperty(required=True)
    publisher = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)


def all_books():
    return Book.query()


def get_book(isbn):
    return Book.query(Book.isbn == isbn).get()
