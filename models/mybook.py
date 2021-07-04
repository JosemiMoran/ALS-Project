from google.appengine.ext import ndb


class MyBook(ndb.Model):
    book = ndb.StringProperty(required=True)
    user = ndb.StringProperty(required=True)


def get_mybook_user(key_book, user):
    return MyBook.query(MyBook.book == key_book and MyBook.user == user).get()


def get_mybooks(user):
    return MyBook.query(MyBook.user == user).order()


def create(b):
    book = MyBook()
    book.book = b.book
    book.user = b.user

    return book


def create_empty_book():
    book = MyBook()
    book.book = ""
    book.user = ""

    return book


def create_query_delete_one(book):
    return book.key.delete()


@ndb.transactional
def update(book):
    return book.put()
