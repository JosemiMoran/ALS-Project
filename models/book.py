from google.appengine.ext import ndb


class Book(ndb.Model):
    isbn = ndb.StringProperty(indexed=True, required=True)
    title = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=True)
    year = ndb.IntegerProperty(required=True)
    image = ndb.BlobProperty(required=True)
    publisher = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)


def all_books():
    return Book.query()


def get_book(isbn):
    return Book.query(Book.isbn == isbn).get()


def get_book_key(key_book):
    return ndb.Key(urlsafe=key_book).get()


def create(b):
    book = Book()
    book.isbn = b.isbn
    book.title = b.title
    book.author = b.author
    book.year = b.year
    book.image = b.image
    book.publisher = b.publisher
    book.description = b.description

    return book


def create_empty_book():
    book = Book()
    book.isbn = ""
    book.title = ""
    book.author = ""
    book.year = 0
    book.publisher = ""
    book.description = ""

    return book


@ndb.transactional
def update(book):
    return book.put()
