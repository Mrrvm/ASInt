import lab3_module

class dbUI:
    'BookDatabase interface for user'

    def run(self, bd):
        while True:
            print("Enter your command")
            command = input("> ")
            if command == 'NEW':
                title = input("Book Title > ")
                author = input("Book Author > ")
                year = int(input("Book Year > "))
                b = lab3_module.Book(author, title, year)
                bd.addBook(b)

            elif command == 'QUIT':
                break

        #import bookDB from bookDB
        #remoteBookDB=Pyro4.expose(bookDB)
        #dbObject=remoteBookDB()
        #deamon=Pyro4.Deamon()
        #uri=deamon.register(dbObject,db)
        #print(uri)
        #deamon.requestLoop()
        #db=Pyro.Proxy(ui)
        #ui=bbUI()
        #ui.readcommands()