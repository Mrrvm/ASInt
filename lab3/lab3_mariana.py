
class Book:
    'book class for lab3'
    _id = 0

    def __init__(self, _author = '', _title = '', _year = ''):
        self.author = _author
        self.title = _title
        self.year = _year
        _id +=1
        self.id = _id

class BookDB:

    def __init__(self):
        self.books = {}

    def insert(self, _book):
        self.books[(_book.author, _book.year, _book.id)] = _book.title

    def show(self, _id)
        for book in self.books
            if book.id == _id
                print('Book found\n'+book.title+'\n'+book.author)
                break

    def listAuthors(self)
        for book in self.books


    def print(self):
        print(self.stack)