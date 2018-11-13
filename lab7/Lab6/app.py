from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import bookDB
import json

app = Flask(__name__)
db = bookDB.bookDB("mylib")

@app.route('/')
def hello_world():
    count = len(db.listAllBooks())
    return render_template("mainPage.html", count_books=count)

@app.route('/addBooksForm')
def add_Book_Form():
    return render_template("addBookTemplate.html")

@app.route('/addBook', methods=['POST', 'GET'])
def add_Book():
    if request.method == "GET":
        return str(request.args)
    else:
        return str(request.form)

@app.route('/API/books')
def show_books():
    books = db.listAllBooks()
    return jsonify([ob.__dict__ for ob in books])

@app.route('/API/authors')
def show_authors():
    authors = db.listAllAuthors()
    print(authors)
    return jsonify(authors)

@app.route('/API/books/<id>', methods=['GET'])
def single_book(id):
    book = db.showBook(int(id))
    return jsonify(book.__dict__)

@app.route('/API/authors/<name>')
def single_author(name):
    books = db.listBooksAuthor(name)
    print(books)
    return jsonify([ob.__dict__ for ob in books])

@app.route('/API/authors/<name>/<year>')
def books_of_author_year(name, year):
    books_author = db.listBooksAuthor(name)
    books_year = db.listBooksAuthor(int(year))
    print(books_author)
    print(books_year)
    for b in books_author:
        if b not in books_year:
            books_author.remove(b)
    print(books_author)
    return jsonify([ob.__dict__ for ob in books_author])

if __name__ == '__main__':
    app.run()
