from flask import Flask
from flask import render_template
from flask import request
import bookDB

app = Flask(__name__)
db = bookDB.bookDB("mylib")

@app.route('/')
def hello_world():
    count = len(db.listAllBooks())
    return render_template("mainPage.html", count_books=count)

@app.route('/addBooksForm')
def add_Book_Form():
    return render_template("addBookTemplate.html")

@app.route('/addBook/<Author>&<Title>&<Year>')
def new_Book():
    db.addBook(Author, Title, Year)
    return render_template("addBookTemplate.html")

@app.route('/addBook', methods=['POST', 'GET'])
def add_Book():
    if request.method == "GET":
        return str(request.args)
    else:
        author = request.form["Author"]
        title = request.form["Title"]
        year = request.form["Year"]
        db.addBook(author, title, year)
        return str(request.form)
    return render_template("addBookTemplate.html")


if __name__ == '__main__':
    app.run()
