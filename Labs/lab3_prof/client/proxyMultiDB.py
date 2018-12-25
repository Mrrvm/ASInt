class proxyMultiDB:
    def __init__(self, db_list):
        self.db_list = db_list

        def addBook(self, author, title, year):
            for i in range(len(db_list)):
                db_list[i].addBook(author, title, year)

        def listAllBooks(self):
            all_books = []
            for i in range(len(db_list)):
                all_books.append(db_list[i].listAllBooks())
            return all_books