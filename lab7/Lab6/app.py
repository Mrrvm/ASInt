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
    return render_template("addBookTemplate.html")

@app.route('/API/books')
def show_books(): 
    books = db.listAllBooks()
    return jsonify([ob.__dict__ for ob in books])

@app.route('/API/authors')
def show_authors():
    authors = db.listAllAuthors()
    print(authors)
    return jsonify([ob.__dict__ for ob in authors])

@app.route('/API/books/<id>', methods=['GET'])
def single_book():
    _id = str(request.data)
    print(_id)
    book = db.showBook(_id)
    print(book)
    return jsonify(book)

#@app.route('/API/authors/<name>')
#def single_author(): 
#@app.route('/API/authors/<name>/year/<year>')
#def books_of_author_year(): 

if __name__ == '__main__':
    app.run()
