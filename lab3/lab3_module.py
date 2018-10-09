
class Book:
    'Book class for lab3'
    book_id = 0

    def __init__(self, author='', title='', publication_year=2018):
        self.author = author
        self.title = title
        self.publication_year = publication_year
        Book.book_id += 1
        self.identifier = Book.book_id

    def print(self):
        print("Title: " + self.title + "\nAuthor: " + self.author + "\nYear: " + str(self.publication_year))


class BookDB:
    'BookDB class for lab3'

    def __init__(self):
        self.books = []

    def addBook(self, b):
        nb = Book()
        nb.author = b.author
        nb.title = b.title
        nb.publication_year = b.publication_year
        nb.identifier = b.identifier
        self.books.append(nb)


    #def showBook(self, identifier):


    #def list_authors(self, x):


    #def search_author(self, x):


    #def search_year(self, x):

